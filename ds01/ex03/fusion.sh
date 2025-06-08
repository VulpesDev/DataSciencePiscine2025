#!/bin/bash

set -a
. ../.env
set +a

TABLE_NAME="customers"
ITEM_TABLE_NAME="item"
TEMP_TABLE_NAME="temp_fusion"
start=$(date +%s.%N)

FUSE_TEMP_TABLE="CREATE TABLE $TEMP_TABLE_NAME AS
    WITH merged AS (
      SELECT
        product_id,
        MAX(category_id) AS category_id,
        MAX(category_code) AS category_code,
        MAX(brand) AS brand
      FROM $ITEM_TABLE_NAME
      GROUP BY product_id
      )
      SELECT
      tbname.*,
      m.category_id,
      m.category_code,
      m.brand
    FROM $TABLE_NAME tbname
    LEFT JOIN merged m ON tbname.product_id = m.product_id;"

DROP_OLD_TABLE="DROP TABLE $TABLE_NAME;"

RENAME_TEMP_TABLE="ALTER TABLE $TEMP_TABLE_NAME RENAME TO $TABLE_NAME;"

execute_in_container() {
    echo "Executing fusion command..."
    docker exec -i $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB <<EOF
    BEGIN;
    $FUSE_TEMP_TABLE
    $DROP_OLD_TABLE
    $RENAME_TEMP_TABLE
    COMMIT;
EOF
}

execute_in_container

end=$(date +%s.%N)
elapsed=$(echo "$end - $start" | bc)
echo "Execution time: $elapsed seconds"