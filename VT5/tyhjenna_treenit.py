from mod_python import apache
from pysqlite2 import dbapi2 as sqlite
import os
import sys

def index(req):
    if req.session["kirjautunut"] == "ok":
       con = sqlite.connect('/nashome3/sajukaru/html/hidden/kanta/kanta')
       con.text_factory = str
       con.row_factory = sqlite.Row
       # sleep jotta latauksen indikaattori n‰kyisi pidemp‰‰n
       time.sleep(1)
       req.content_type = "text/plain; charset=UTF-8"
       
       sql = """
             DELETE FROM Treeni
       """
       
       cur = con.cursor()
       moi = ""
       try:
          cur.execute(sql)
          con.commit()   
       except:
          req.write(str(sys.exc_info()[0]))
          
       con.close() 
       return