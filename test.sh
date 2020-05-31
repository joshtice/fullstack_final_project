#!/usr/bin/env bash

export APP_MODE=test

psql -f tests/setup_test_db.sql
pytest -vv
psql -f tests/teardown_test_db.sql 

export APP_MODE=development
 
