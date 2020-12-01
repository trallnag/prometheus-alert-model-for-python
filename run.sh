#!/usr/bin/env bash

project_name="prometheus_alert_model"

# ==============================================================================
# Misc

docs () {
    tmp_dir=/tmp/docs
    rm -rf /tmp/docs
    mkdir -p /tmp/docs
    rm -rf docs/*
    mkdir -p docs
    poetry run pdoc --output-dir /tmp/docs --html ${project_name}
    mv /tmp/docs/${project_name}/* docs/
    rm -rf /tmp/docs
}

lint () {
    poetry run flake8 --config .flake8 --statistics
    poetry run mypy ${project_name} --allow-redefinition
}

requirements () {
    poetry export \
        --format "requirements.txt" \
        --output "requirements.txt" \
        --without-hashes
}

# ==============================================================================
# Format

format_style () {
    poetry run black .    
}

format_imports () {
    poetry run isort --profile black .
}

format () {
    format_style
    format_imports
}

# ==============================================================================
# Test

test_not_slow () {
    poetry run pytest -m "not slow"
}

test_slow () {
    poetry run pytest -m "slow"
}

test () {
    test_not_slow
    test_slow
}

# ==============================================================================

help () {
    cat << EOF
docs
lint
requirements
format_style
format_imports
format
test_not_slow
test_slow
test
EOF
}

# This lets you do ./run.sh build foo bar at the command line.  The autocomplete
# scans for functions in .sh files and fills them in as the first arg.

"$@"
