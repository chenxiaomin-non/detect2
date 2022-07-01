import os
import hashlib


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

depends = open(PROJECT_DIR + '/.depend' , 'r')
for line in depends:
    os.system('pip install %s' % line.strip())

IP_ADDR = 'localhost'
PORT = '8000'

HASH = hashlib.sha256()
SECRET_CODE = b'\xed\x8a\x05A\xad\xfc\xd4\xd8%\x0f\xbf\xd5\xee\x07\xe5$\x03\xae\xf5\x05\xa0\x80\xb2\xf3)\x9cqP\xd0\x90=['

DB_IN_USED = 'cmc_token2'


