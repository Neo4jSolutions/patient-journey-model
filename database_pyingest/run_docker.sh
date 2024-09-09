#     -v ./plugins:/plugins \

docker run --rm \
    -p 7474:7474 -p 7687:7687 \
    -v ./data:/data \
    -v ./import:/import \
    --name neo4j_patient_journey \
    -e NEO4J_AUTH=neo4j/neo4j123 \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -e NEO4J_dbms_security_procedures_unrestricted="apoc.*" \
    -e NEO4J_AUTH=neo4j/neo4j123 \
    -e EXTENDED_CONF=yes \
    -e NEO4J_ACCEPT_LICENSE_AGREEMENT=yes \
    neo4j:enterprise