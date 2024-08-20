# Ingestion using PyNeoInstance

* Configure neo4j details and directory to synthea data in [config-pyneoinstance.yaml](config-pyneoinstance.yaml)

* Run below (Poetry required)
```shell
# install dependencies and source into virtualenv
poetry install --no-root
poetry shell

python main.py
```