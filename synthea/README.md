# Obtaining Patient Journey Data from Synthea

Data such as is used in the demo can be obtained from Synthea using the following steps:

* Clone or download the Synthea project from [github](https://github.com/synthetichealth/synthea)

* Replace `src/main/resources/synthea.properties` with the `synthea.properties` file in this folder.  
This configures Synthea to generate only csv files.

* From the root folder of your Synthea project checkout, run the following command:
`./run_synthea -p 1000000`
where `p` is the number of synthetic patients you wish to generate.

* Once you have generated the synthetic patients, see [here](../ingest/README.md) for details on loading the
data into Neo4j.