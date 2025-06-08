#!/bin/bash

set -a
. ../.env
set +a

#POPULATE DATA

#Load CSV files
CSV_FILES=$(find "../subject/customer" \
                    "../subject/item" -maxdepth 1 -type f -name "*.csv")

get_table_name() {
    local base=${1##*/}
    local result=${base%.*}
    echo "$result"
}

load_data() {
    local table_name="$1"
    local csv_path="$2"
    local args=$(head -n 1 "$2")
    
    docker exec -i $POSTGRES_CONTAINER \
    psql -U $POSTGRES_USER -d $POSTGRES_DB -v ON_ERROR_STOP=1 -c "\copy ${table_name} ($args) From STDIN DELIMITER ',' CSV HEADER;" < $csv_path
}

set -- $CSV_FILES
for csv_path in "$@"; do
    table_name=$(get_table_name ${csv_path})
    echo "-- Populating table: $table_name"
    load_data $table_name ${csv_path}
done
