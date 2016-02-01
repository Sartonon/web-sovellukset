from mod_python import apache
from pysqlite2 import dbapi2 as sqlite
import os
import sys
import simplejson as json

def index(req):
    if req.session["kirjautunut"] == "ok":
       con = sqlite.connect('/nashome3/sajukaru/html/hidden/kanta/kanta')
       con.text_factory = str
       con.row_factory = sqlite.Row
       req.content_type = "application/json; charset=UTF-8"
       sql = """
             SELECT TreenityyppiID, Treenityyppinimi
             FROM Treenityyppi
       """
       treenityypit = {}
       cur = con.cursor()
       try:
          cur.execute(sql)   
       except:
          req.write(str(sys.exc_info()[0]))
          
       for rivi in cur:
          treenityypit[rivi["TreenityyppiID"]] =  str(rivi["Treenityyppinimi"])
           
           
       req.write(json.dumps(treenityypit))
       
       return