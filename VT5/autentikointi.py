# -*- coding: UTF-8 -*-
from mod_python import apache, Session
from mod_python import util
from pysqlite2 import dbapi2 as sqlite
import sys
import os
import sha

# Hoitaa kirjautumisen (koodiin saattanut j‰‰d‰ ylim‰‰r‰isi‰ juttuja edellisest‰ viikkoteht‰v‰st‰ mutta toimii.
def index(req):
        con = sqlite.connect( '/nashome3/sajukaru/html/hidden/kanta/kanta')
        con.text_factory = str
        con.row_factory = sqlite.Row
        req.content_type = 'text/plain ;charset=utf-8'
        #req.session.invalidate()
        
        try:
           if req.session["kirjautunut"] == "ok":
              req.write(req.session["kayttaja"] + "|")
              req.write(req.session["nimi"] + "|")
              return apache.OK
                        
        except:
           #form = util.FieldStorage(req)
           email = req.form.getfirst("tunnus")
           salasana = req.form.getfirst("salasana")
           hash = sha.new()
           hash.update(email)
           hash.update(salasana)
           salasana1 = hash.hexdigest()
           salsu = 0
           emailt = 0
           
           if email == "":
              return apache.DONE
           
           sql = """
           SELECT Email
           FROM Henkilo
           WHERE Email = :email
           """
           
           cur = con.cursor()
           try:
              cur.execute(sql, {"email":email})
           except: 
              # vaatii koodin alkuun rivin: import sys
              req.write("nyt tuli virhe: %s" % sys.exc_info()[0])
           
           sql = """
                 SELECT Email
                 FROM Henkilo
                 WHERE Salasana = :salasana
                 """
           for rivi in cur:
              emailt = 1
             # cur = con.cursor()
              try:
                 cur.execute(sql, {"salasana":salasana1})
              except: 
                # vaatii koodin alkuun rivin: import sys
                req.write("nyt tuli virhe: %s" % sys.exc_info()[0])
              for rivi1 in cur:
                 salsu = 1
           
           if (salsu == 1 and emailt == 1):
              sql = """
                    SELECT Email, Salasana, Etunimi, Sukunimi
                    FROM Henkilo
                    WHERE Email = :email AND Salasana = :salasana
                    """
              try:
                 cur.execute(sql, {"email":email, "salasana":salasana1})
              except: 
                # vaatii koodin alkuun rivin: import sys
                req.write("nyt tuli virhe: %s" % sys.exc_info()[0])
              
              for rivi in cur:                   
                 req.session["kirjautunut"] = "ok"
                 req.session["kayttaja"] = email
                 req.write(email + "|")
                 req.session["nimi"] = rivi["etunimi"] + " " + rivi["sukunimi"]
                 req.write(req.session["nimi"] + "|")
                 req.session.save()
                 return apache.OK
          
           if (salsu == 0 and emailt == 1):
              return apache.DONE
              
           if (salsu == 0 and emailt == 0):
              return apache.DONE      
           else:
              return apache.DONE
        else:
            return apache.DONE    