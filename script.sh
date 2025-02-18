#!/bin/bash
set -e  # Stops the script if any command fails

echo "Starting execution..."

python src/EDA.py
echo "EDA.py completed."

python src/Scoring.py
echo "Scoring.py completed."

python src/base_clustering.py
echo "base_clustering.py completed."

python src/Embedding.py
echo "Embedding.py completed."

python src/Advance_clustering.py
echo "Advance_clustering.py completed."

echo "Execution complete!"
