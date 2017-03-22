#!/usr/bin/python
import sys
import logging
logging.basicConfig(steram=sys.stderr)
sys.path.insert(0,"/var/www/idb/idb/")
from app import app as application
application.secret_key = "This key is very secret"
