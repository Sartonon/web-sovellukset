from mod_python import apache
from pysqlite2 import dbapi2 as sqlite
import os
import sys
import simplejson as json
import time

def index(req):
    if req.session["kirjautunut"] == "ok":
       #time.sleep(1)
       con = sqlite.connect('/nashome3/sajukaru/html/hidden/kanta/kanta')
       con.text_factory = str
       con.row_factory = sqlite.Row
       req.content_type = "application/json; charset=UTF-8"
       email = "tommi.j.lahtonen@jyu.fi"
       sql = """
             SELECT *
             FROM Treeni
             LEFT OUTER JOIN tyyppia ON treeni.treeniID = tyyppia.treeniID 
             LEFT OUTER JOIN treenityyppi ON tyyppia.treenityyppiID = treenityyppi.treenityyppiID 
             LEFT OUTER JOIN lajia ON lajia.treeniID = treeni.treeniID 
             LEFT OUTER JOIN laji ON lajia.lajiID = laji.lajiID
             LEFT OUTER JOIN Henkilo ON Henkilo.Email = Treeni.Email
             ORDER BY Treeni.Alkuaika
       """
       treenit = {}
       cur = con.cursor()
       moi = ""
       try:
          cur.execute(sql)   
       except:
          req.write(str(sys.exc_info()[0]))
          
       for rivi in cur:
          nimi = str(rivi["Etunimi"]) + " " + str(rivi["Sukunimi"])
          
          try:
            nopeus = float(rivi["kesto"]) / float(rivi["Km"])
            nopeus = round(nopeus, 2)
            nopeus = str(nopeus) + " min/km"
          except:
            nopeus = "N/A"
          treenit[rivi["TreeniID"]] = str(rivi["TreeniID"]) + "|" + nimi + "|" + str(rivi["Treenityyppinimi"]) + "|" + str(rivi["Lajinimi"])  + "|" + str(rivi["Alkuaika"]) + "|" + str(rivi["kesto"]) + "|" + str(rivi["Km"]) + "|" + str(nopeus) + "|" + str(rivi["Syke_avg"]) + "|" + str(rivi["Syke_max"]) + "|" + str(rivi["Kalorit"]) + "|" + str(rivi["Kommentti"])
           
           
       req.write(json.dumps(treenit))
       
       return