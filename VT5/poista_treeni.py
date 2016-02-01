from mod_python import apache
from pysqlite2 import dbapi2 as sqlite
import os
import sys
import time

def index(req):
    if req.session["kirjautunut"] == "ok":
       # latauksen indikaattoria varten
       time.sleep(1)
       con = sqlite.connect('/nashome3/sajukaru/html/hidden/kanta/kanta')
       con.text_factory = str
       con.row_factory = sqlite.Row
       
       req.content_type = "text/plain; charset=UTF-8"
       treeniid = req.form.getfirst("treeniid");
       
       sql = """
             DELETE FROM Treeni
             WHERE TreeniID = :treeniid
       """
       treenityypit = {}
       cur = con.cursor()
       try:
          cur.execute(sql, {"treeniid": treeniid})
          con.commit()
          req.write("poisto onnistui")    
       except:
          req.write(str(sys.exc_info()[0]))
          req.write("poisto ei onnistunut")       
       
       
       return