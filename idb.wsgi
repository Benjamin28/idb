#!/usr/bin/env python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/idb/idb/")
activate_this = '/var/www/idb/idb/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
from app import app as application
application.secret_key = "This key is very secret"
