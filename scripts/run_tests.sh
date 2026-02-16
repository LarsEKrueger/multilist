#! /usr/bin/bash -xe

# Script to run the test suite

# Get the base dir
REPO_DIR=$(dirname $(git rev-parse --absolute-git-dir))
echo $REPO_DIR
RUN_DIR=${REPO_DIR}/.test_runs
mkdir -p $RUN_DIR
TEST_DIR=${REPO_DIR}/tests

rm -f ${RUN_DIR}/*.json

export PYTHONPATH="$REPO_DIR/src:$PYTHON_PATH"
python3 ${TEST_DIR}/01_database.py $RUN_DIR/01.json
