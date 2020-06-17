# Ingesting Patient Journey Data into Neo4j

Having obtained synthetic patient journey data from Synthea (see [here](../synthea/README.md)), you can 
follow these steps to ingest the data to a Neo4j graph:

* Prerequisites - Python 3, Pip, Neo4j 3.5.x, APOC plugin

* Clone or download the `pyingest` project from github [here](https://github.com/mholford-neo/pyingest)

* Obtain dependencies by running: `pip3 install -r requirements.txt`

* Modify the `config.yml` file in this folder to specify your Neo4j connection information and also the 
location of the CSV files from Synthea

* From the root folder of your pyinstall checkout run: 
`python3 src/main/ingest.py $JOURNEY_DEMO/ingest/config.yml`, where `$JOURNEY_DEMO` is the path to the root of this project.

* If you get complains about missing module yaml, run the following: `pip3 install pyyaml`


### Neo4j configuration notes

For running the full 1 million patient demo, we use a dedicated AWS instance with 16 CPU and 128G RAM.
Neo4j is installed on a detachable SSD volume.  For this volume of data, we recommend setting the 
following in `neo4j.conf`:

* dbms.memory.heap.initial_size=31g
* dbms.memory.heap.max_size=31g
* dbms.memory.pagecache.size=80g
