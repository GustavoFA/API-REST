#!/bin/bash

set -e

DATA_DIR="./data"
ZIP_FILE="$DATA_DIR/ecommerce-data.zip"

mkdir -p "$DATA_DIR"

kaggle datasets download -d carrie1/ecommerce-data -p "$DATA_DIR"

unzip -o "$ZIP_FILE" -d "$DATA_DIR"

rm "$ZIP_FILE"

echo "Done. Files extracted to $DATA_DIR"