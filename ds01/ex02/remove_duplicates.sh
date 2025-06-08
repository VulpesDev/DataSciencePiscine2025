#!/bin/bash

set -a
. ../.env
set +a

TABLE_NAME="customers"
start=$(date +%s.%N)

remove_duplicate_data() {
    REMOVE_DUPLICATES_SQL="DELETE FROM $TABLE_NAME a
    USING $TABLE_NAME b
    WHERE a.ctid > b.ctid
	AND a.event_type = b.event_type
    AND a.product_id = b.product_id
    AND a.user_id = b.user_id
	AND a.user_session = b.user_session
    AND ABS(EXTRACT(EPOCH FROM a.event_time - b.event_time)) <= 1;"

    docker exec -i $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB <<EOF
    $REMOVE_DUPLICATES_SQL
EOF
}

echo "Remove duplicate data from $TABLE_NAME"
remove_duplicate_data

end=$(date +%s.%N)
elapsed=$(echo "$end - $start" | bc)
echo "Execution time: $elapsed seconds"