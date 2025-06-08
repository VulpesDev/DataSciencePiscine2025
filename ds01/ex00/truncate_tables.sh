#!/bin/bash
set -a
. ../.env
set +a

CSV_FILES=$(find "/home/tvasilev/sgoinfre/subject/customer" -maxdepth 1 -type f -name "*.csv")

get_table_name() {
    local base=${1##*/}
    local result=${base%.*}
    echo "$result"
}

truncate_data() {
    local table_name="$1"
    
    docker exec -i $POSTGRES_CONTAINER \
    psql -U $POSTGRES_USER -d $POSTGRES_DB -v ON_ERROR_STOP=1 <<SQL
    TRUNCATE TABLE ${table_name};
SQL
}

set -- $CSV_FILES
for csv_path in "$@"; do
    table_name=$(get_table_name ${csv_path})
    echo "-- Truncating table: $table_name"
    truncate_data $table_name ${csv_path}
done