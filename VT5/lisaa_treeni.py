from mod_python import apache
from pysqlite2 import dbapi2 as sqlite
import os
import sys
import time

def index(req):
    if req.session["kirjautunut"] == "ok":
      con = sqlite.connect('/nashome3/sajukaru/html/hidden/kanta/kanta')
      con.text_factory = str
      con.row_factory = sqlite.Row
      req.content_type = "text/plain; charset=UTF-8"
      # latauksen indikaattoria varten sleep
      time.sleep(1)
      email = req.form.getfirst("email")
      alkuaika = req.form.getfirst("alkuluku")
      kesto = req.form.getfirst("kesto")
      km = req.form.getfirst("km")
      keskisyke = req.form.getfirst("keskisyke")
      sykemax = req.form.getfirst("sykemax")
      kalorit = req.form.getfirst("kalorit")
      kommentti = req.form.getfirst("kommentti")
      laji = req.form.getfirst("laji")
      treenityyppi = req.form.getfirst("treenityyppi")
      
      sql = """
            INSERT INTO Treeni (Alkuaika, kesto, Km, Syke_avg, Syke_max, Kalorit, Kommentti, Email)
            VALUES (:alkuaika, :kesto, :km, :keskisyke, :sykemax, :kalorit, :kommentti, :email)
      """
      
      sql2 = """
             INSERT INTO lajia (TreeniID, LajiID)
             VALUES (:treeniid, :laji)
      """
      
      sql3 = """
             INSERT INTO tyyppia (TreeniID, TreenityyppiID)
             VALUES (:treeniid, :treenityyppi)
      """
      
      cur = con.cursor()
      moi = ""
      try:
         cur.execute(sql, {"alkuaika":alkuaika, "kesto":kesto, "km":km, "keskisyke":keskisyke, "sykemax":sykemax,
                            "kalorit":kalorit, "kommentti":kommentti, "email":email})
                            
         treeniid = cur.lastrowid
         cur.execute(sql2, {"treeniid": treeniid, "laji": laji})
         
         cur.execute(sql3, {"treeniid": treeniid, "treenityyppi": treenityyppi})
                
         con.commit()     
      except:
         req.write(str(sys.exc_info()[0]))
         return
         
      con.close()
      req.write("onnistui")
      return