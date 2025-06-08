#!/bin/bash

set -a
. ../.env
set +a

CSV_FILES=$(find "../subject/customer" -maxdepth 1 -type f -name "*.csv")

get_table_name() {
    local base=${1##*/}
    local result=${base%.*}
    echo "$result"
}

create_table() {
    local table_name=$1
    
    # Create table SQL command

    SQL=" CREATE TABLE IF NOT EXISTS $table_name (
        event_time TIMESTAMP WITH TIME ZONE,
        event_type TEXT,
        product_id INTEGER,
        price NUMERIC(10,2),
        user_id BIGINT,
        user_session UUID
    );"

    docker exec -i $POSTGRES_CONTAINER \
    psql -U $POSTGRES_USER -d $POSTGRES_DB -v ON_ERROR_STOP=1 <<EOF
$SQL
EOF
}
set -- $CSV_FILES
for table_name in "$@"; do
    echo "-- Creating table: $(get_table_name ${table_name})"
    create_table $(get_table_name ${table_name})
done