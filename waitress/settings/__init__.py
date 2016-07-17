import os

if os.getenv('OPENSHIFT_PYTHON_DIR'):
    from staging import *
