import os
import hashlib
import sys

print(sys.path)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


IP_ADDR = '127.0.0.1'
PORT = 8234

HASH = hashlib.sha256()
SECRET_CODE = b'\xed\x8a\x05A\xad\xfc\xd4\xd8%\x0f\xbf\xd5\xee\x07\xe5$\x03\xae\xf5\x05\xa0\x80\xb2\xf3)\x9cqP\xd0\x90=['

DB_IN_USED = 'cmc_token2'


