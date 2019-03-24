import etcd
import os
import base64

from datetime import datetime, timedelta

start_date = datetime(2019, 1, 21)
end_date = datetime.today() - timedelta(days=2)

DEVELOPMENT = os.environ.get("DEVELOPMENT", "")

ETCD_PROTOCOL = os.environ["ETCD_PROTOCOL"]
ETCD_HOST = os.environ["ETCD_HOST"]
ETCD_PORT = os.environ["ETCD_PORT"]
client = etcd.Client(protocol=ETCD_PROTOCOL, host=ETCD_HOST, port=int(ETCD_PORT))

# Generic
# DEBUG = client.get("/vars/DEBUG").value
DEBUG = True
ETCD_URL = client.get("/vars/ETCD_URL").value

# Database Credentials
PRODDB_URL = client.get("/vars/PRODDB_URL").value
STAGINGDB_URL = client.get("/vars/STAGINGDB_URL").value
SANDBOXDB_URL = client.get("/vars/SANDBOXDB_URL").value
DEVDB_URL = client.get("/vars/DEVDB_URL").value
DATADB_URL = client.get("/vars/DATADB_URL").value

# AWS Bucket Names
AWS_BUCKET_NAME = client.get("/vars/AWS_BUCKET_NAME").value
AWS_APP_BUCKET_NAME = client.get("/vars/AWS_APP_BUCKET_NAME").value

# AWS Credentials
# if access and secret keys don"t exist than try using an IAM role
try:
    AWS_ACCESS_KEY_ID = client.get("/vars/AWS_ACCESS_KEY_ID").value
    AWS_SECRET_ACCESS_KEY = client.get("/vars/AWS_SECRET_ACCESS_KEY").value
    AWS_SECURITY_TOKEN = client.get("/vars/AWS_SECURITY_TOKEN").value
    AWS_SESSION_TOKEN = client.get("/vars/AWS_SESSION_TOKEN").value
except etcd.EtcdKeyNotFound:
    IAM_ROLE = client.get("/vars/IAM_ROLE").value
    AWS_ACCESS_KEY_ID = None
    AWS_SECRET_ACCESS_KEY = None
    AWS_SECURITY_TOKEN = None
    AWS_SESSION_TOKEN = None

env_dict = {
            "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
            "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
            "AWS_SESSION_TOKEN": AWS_SESSION_TOKEN,
            "AWS_SECURITY_TOKEN": AWS_SECURITY_TOKEN,
            "AWS_BUCKET_NAME": AWS_BUCKET_NAME,
            "AWS_APP_BUCKET_NAME": AWS_APP_BUCKET_NAME,
            "DATADB_URL": DATADB_URL,
            "DEVDB_URL": DEVDB_URL,
            "DEVELOPMENT": DEVELOPMENT,
            "DEBUG": DEBUG,
            "IAM_ROLE": IAM_ROLE,
            "PRODDB_URL": PRODDB_URL,
            "SANDBOXDB_URL": SANDBOXDB_URL,
            "STAGINGDB_URL": STAGINGDB_URL}

# remove key/value pairs where value is None
environment = {a: b for a, b in zip(env_dict.keys(), env_dict.values()) if b}
