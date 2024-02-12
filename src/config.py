import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST: str | None = os.environ.get('DB_HOST', 'localhost')
DB_PORT: str | None = os.environ.get('DB_PORT', '5432')
DB_NAME: str | None = os.environ.get('DB_NAME', 'my_database')
DB_USER: str | None = os.environ.get('DB_USER', 'my_user')
DB_PASS: str | None = os.environ.get('DB_PASS', 'my_password')

DB_HOST_TEST: str | None = os.environ.get('DB_HOST_TEST', 'localhost')
DB_PORT_TEST: str | None = os.environ.get('DB_PORT_TEST', '5432')
DB_NAME_TEST: str | None = os.environ.get('DB_NAME_TEST', 'test_database')
DB_USER_TEST: str | None = os.environ.get('DB_USER_TEST', 'test_user')
DB_PASS_TEST: str | None = os.environ.get('DB_PASS_TEST', 'test_password')

REDIS_HOST: str | None = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT: str | None = os.environ.get('REDIS_PORT', '6379')
