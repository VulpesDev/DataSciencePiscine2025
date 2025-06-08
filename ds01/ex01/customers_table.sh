#!/bin/bash
set -a
. ../.env
set +a

MERGED_TABLE="customers"
CSV_FILES=$(find "../subject/customer" -maxdepth 1 -type f -name "*.csv")
start=$(date +%s.%N)

get_table_name() {
    local base=${1##*/}
    local result=${base%.*}
    echo "$result"
}

truncate_data() {
    TRUNCATE_TABLE_SQL="TRUNCATE TABLE $MERGED_TABLE;"
    docker exec -i $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB <<EOF
    $TRUNCATE_TABLE_SQL
EOF
}

load_data() {
    local table_name="$1"

    # Construct SQL
    CREATE_TABLE_SQL="CREATE TABLE IF NOT EXISTS $MERGED_TABLE (LIKE $table_name);"
    INSERT_SQL="INSERT INTO $MERGED_TABLE SELECT * FROM $table_name;"

    # Execute in Docker
    docker exec -i $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB <<EOF
    $CREATE_TABLE_SQL
    $INSERT_SQL
EOF
}

truncate_data

set -- $CSV_FILES
for csv_path in "$@"; do
    table_name=$(get_table_name ${csv_path})
    echo "-- Populating table: $MERGED_TABLE with data from $table_name"
    load_data $table_name
done

end=$(date +%s.%N)
elapsed=$(echo "$end - $start" | bc)
echo "Execution time: $elapsed seconds"

