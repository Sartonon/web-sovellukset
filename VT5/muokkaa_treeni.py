from mod_python import apache
from pysqlite2 import dbapi2 as sqlite
import os
import sys
import time

def index(req):
    # Treenin muokkaus
    if req.session["kirjautunut"] == "ok":
       con = sqlite.connect('/nashome3/sajukaru/html/hidden/kanta/kanta')
       con.text_factory = str
       con.row_factory = sqlite.Row
       req.content_type = "text/plain; charset=UTF-8"
       time.sleep(1)
       id = req.form.getfirst("id")
       
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
       
       # Treenitaulun käsky
       sql = """
             UPDATE Treeni SET Alkuaika = :alkuaika, kesto = :kesto, Km = :km, Syke_avg = :keskisyke, Syke_max = :sykemax, Kalorit = :kalorit, Kommentti= :kommentti, Email = :email
             WHERE TreeniID = :id
       """
       
       # Lajin käsky
       sql2 = """
              UPDATE lajia SET LajiID = :laji
              WHERE TreeniID = :id
       """
       
       # Treenityypin käsky
       sql3 = """
              UPDATE tyyppia SET TreenityyppiID = :treenityyppi
              WHERE TreeniID = :id
       """
       
       cur = con.cursor()
       moi = ""
       try:
          cur.execute(sql, {"alkuaika":alkuaika, "kesto":kesto, "km":km, "keskisyke":keskisyke, "sykemax":sykemax,
                             "kalorit":kalorit, "kommentti":kommentti, "id":id, "email":email})
                             
          treeniid = cur.lastrowid
          cur.execute(sql2, {"laji": laji, "id": id})
          
          cur.execute(sql3, {"treenityyppi": treenityyppi, "id": id})
                 
          con.commit()     
       except:
          req.write(str(sys.exc_info()[0]))
          return
          
       con.close()
       req.write("onnistui")
       return