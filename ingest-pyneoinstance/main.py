import os
import time
import traceback
from datetime import datetime

import pandas as pd

# from openpyxl import load_workbook
from pandas import DataFrame
from pyneoinstance import Neo4jInstance
from pyneoinstance.fileload import load_yaml_file

BATCH_SIZE = 1000
DEFAULT_WORKERS = 1
POST_INGEST_WAIT = 10


def main():
    print_()

    cf = load_yaml_file("config-pyneoinstance.yaml")

    data_directory = cf["data_directory"]
    dbname = cf["database"]

    print_(f"server_uri = {cf['server_uri']}")
    print_(f"admin_user = {cf['admin_user']}")
    print_(f"admin_pass = {cf['admin_pass']}")
    print_(f"database = {dbname}")
    print_(f"Import directory = {data_directory}")
    input("\nContinue? ")

    # pre validate config yaml
    has_loading_queries = (
        cf.get("loading_queries", None)
        and cf.get("loading_queries", None).get("nodes", None)
    ) is not None
    if has_loading_queries:
        node_load_queries = cf["loading_queries"]["nodes"]
        for node_name, v in node_load_queries.items():
            fp = os.path.join(data_directory, v["file"])
            if not os.path.isfile(fp):
                print(f"File <{fp}>  not found")
                exit(1)

    start = time.time()  # seconds
    graph = Neo4jInstance(cf["server_uri"], cf["admin_user"], cf["admin_pass"])

    # pre ingest
    print_("Running pre_ingest queries...")
    try:
        graph.execute_write_queries(database=dbname, queries=cf["pre_ingest"])
    except Exception as e:
        print_(e)

    # main ingest
    if has_loading_queries:
        for node_name, v in node_load_queries.items():
            print_(f"Nodes: {node_name}")
            if v.get("skip", False):
                print_("   skipped")
                continue
            print_(f"   Reading {v['file']} to dataframe...")
            data = pd.read_csv(os.path.join(data_directory, v["file"]))
            print_("   Getting partitions...")
            partitions = get_partition(data)
            print_(f"   {partitions} partitions")
            print_("   Running ingest query...")
            graph.execute_write_query_with_data(
                database=dbname,
                data=data,
                query=v["query"],
                partitions=partitions,
                parallel=True,
                workers=v.get("workers", DEFAULT_WORKERS),
            )
            print_("   Done")

    if "post_ingest" in cf:
        if has_loading_queries:
            # wait before post ingest
            print_(f"Sleeping for {POST_INGEST_WAIT}s before post ingest...")
            time.sleep(POST_INGEST_WAIT)

        # post ingest
        print_("Running post_ingest queries...")
        try:
            for qry in cf["post_ingest"]:
                print(f"\nRunning: {qry}")
                graph.execute_write_query(qry, database=dbname)
        except Exception as e:
            print_("ERROR")
            traceback.print_exc()
        duration_sec = time.time() - start
        print_(f"Done in {duration_sec} s (about {int(duration_sec / 60)} min)")


def get_partition(data: DataFrame, batch_size: int = BATCH_SIZE) -> int:
    """
    Determine the data partition based on the desired batch size.
    """
    len_data = len(data)
    print_(f"   {len_data} rows")
    partition = int(len_data / batch_size)
    return partition if partition > 1 else 1


def print_(*args):
    print(f"{datetime.now().isoformat()} -", ", ".join(map(str, args)))


if __name__ == "__main__":
    main()
