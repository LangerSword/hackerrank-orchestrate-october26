#!/usr/bin/env sh
# Fetch the participant-facing dataset from the official starter repo.
set -eu
cd "$(dirname "$0")/.."
if [ -d dataset ]; then echo "dataset/ already present"; exit 0; fi
git clone --depth 1 https://github.com/interviewstreet/hackerrank-orchestrate-october26.git .dataset-src
ln -s .dataset-src/dataset dataset
echo "dataset/ linked to .dataset-src/dataset"
