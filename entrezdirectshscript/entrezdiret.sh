#!/bin/bash

# Check if the correct number of arguments is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <nuccore_query>"
    exit 1
fi

# Assign the parameter to a variable for readability
nuccore_query="$1"

# Function to query data and check length
function query_data() {
    esearch -db nuccore -query "$nuccore_query" | elink -target assembly | esummary | xtract -pattern DocumentSummary -element RefSeq
}

# Retry logic
function retry_query_data() {
    retries=5
    while [ $retries -gt 0 ]; do
        output=$(query_data)
        if [ ${#output} -ge 3 ]; then
            echo "$output"
            return
        fi
        retries=$((retries - 1))
        sleep 1
    done
    echo "No output with length >= 3 after retries."
    exit 1
}

# Run the retry logic
retry_query_data