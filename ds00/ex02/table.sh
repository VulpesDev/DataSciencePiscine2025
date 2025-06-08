#!/bin/bash
set -a
. ../.env
set +a

CSV_FILE="../subject/customer/data_2022_oct.csv"

get_table_name() {
    local base=${1##*/}
    local result=${base%.*}
    echo "$result"
}

TABLE_NAME=$(get_table_name "$CSV_FILE")

# Define SQL commands
SQL="
-- Create table with explicit types
CREATE TABLE IF NOT EXISTS $TABLE_NAME (
    event_time TIMESTAMP WITH TIME ZONE,
    event_type TEXT,
    product_id INTEGER,
    price NUMERIC(10,2),
    user_id BIGINT,
    user_session UUID
);"

echo "Creating table " $TABLE_NAME
# Execute SQL commands
docker exec -i $POSTGRES_CONTAINER \
psql -U $POSTGRES_USER -d $POSTGRES_DB -v ON_ERROR_STOP=1 <<EOF
$SQL
EOF