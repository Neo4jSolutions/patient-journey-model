# export USER_ID="$(id -u)"
# export GROUP_ID="$(id -g)"
export NEO4J_DOCKER_IMAGE=neo4j:enterprise

# docker cmpose for cluster
export NEO4J_EDITION=docker_compose

export EXTENDED_CONF=yes
export NEO4J_ACCEPT_LICENSE_AGREEMENT=yes
export NEO4J_AUTH=neo4j/neo4j123
docker compose up $1