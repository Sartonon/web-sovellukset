# -*- coding: UTF-8 -*-
from mod_python import apache, Session
from mod_python import util
from pysqlite2 import dbapi2 as sqlite
import sys
import os

# Hoitaa invalidoimisen
def index(req):
        req.content_type = 'text/plain ;charset=utf-8'
        req.session.invalidate()
        
        return apache.DONE