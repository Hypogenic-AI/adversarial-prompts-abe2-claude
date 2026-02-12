#!/bin/bash
# Download the pre-retrieved documents for NQ-Open used by "Lost in the Middle"
#
# This file contains Contriever-MSMARCO retrieved documents for each NQ-Open question.
# It's used to generate multi-document QA examples with varying gold document positions.
#
# Size: ~1.3 GB compressed
# Source: https://github.com/nelson-liu/lost-in-the-middle
#
# After downloading, you can generate new multi-document QA data with:
#   python make_qa_data_from_retrieval_results.py (from the lost-in-the-middle repo)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_FILE="${SCRIPT_DIR}/nq-open-contriever-msmarco-retrieved-documents.jsonl.gz"

echo "Downloading NQ-Open Contriever-MSMARCO retrieved documents..."
echo "This file is approximately 1.3 GB. Download may take several minutes."

curl -L "https://nlp.stanford.edu/data/nfliu/lost-in-the-middle/nq-open-contriever-msmarco-retrieved-documents.jsonl.gz" \
    -o "${OUTPUT_FILE}" \
    --progress-bar

if [ $? -eq 0 ]; then
    echo "Download complete: ${OUTPUT_FILE}"
    echo "File size: $(du -h "${OUTPUT_FILE}" | cut -f1)"
else
    echo "Download failed!"
    exit 1
fi
