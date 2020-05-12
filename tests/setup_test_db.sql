CREATE DATABASE error_logging_app_test;
CREATE USER app_test_user WITH ENCRYPTED PASSWORD 'asdf-asaflkjv';
GRANT ALL PRIVILEGES ON DATABASE error_logging_app_test TO app_test_user;
ALTER USER app_test_user WITH CREATEDB;
ALTER USER app_test_user WITH SUPERUSER;
