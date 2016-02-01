# -*- coding: UTF-8 -*-
from xml.dom.minidom import getDOMImplementation, parse, parseString
from mod_python import apache, Session
from mod_python import util
from pysqlite2 import dbapi2 as sqlite
import sys
import os
import sha

# Hoitaa kirjautumisen
def handler(req):
        con = sqlite.connect( '/nashome3/sajukaru/html/hidden/kanta/kanta')
        con.text_factory = unicode
        con.row_factory = sqlite.Row
        req.content_type = 'text/html ;charset=utf-8'
        pohja = os.path.join(os.path.dirname(req.filename), 'autentikointi.html')
        dom = parse(pohja)
        form = find_element(dom, "form", "form")
        form.setAttribute("action", req.uri)
        try:
           if req.session["kirjautunut"] == "ok":
              #req.session.invalidate()
              return apache.OK
                        
        except:
           form = util.FieldStorage(req)
           email = form.getfirst("tunnus", "kuku")
           salasana = form.getfirst("salasana", "kuku")
           hash = sha.new()
           hash.update(email)
           hash.update(salasana)
           salasana1 = hash.hexdigest()
           salsu = 0
           emailt = 0
           
           if email == "kuku":
              req.write(dom.toxml('UTF-8'))
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
                 req.session["nimi"] = rivi["etunimi"] + " " + rivi["sukunimi"]
                 req.session.save()
                 return apache.OK
          
           if (salsu == 0 and emailt == 1):
              p = find_element(dom, "ilmoitus", "p")
              teksti = "Käyttäjätunnus oikein mutta salasana väärin"
          
              text = dom.createTextNode(teksti.decode("UTF-8"))
              p.appendChild(text)
              req.write(dom.toxml('UTF-8'))
              return apache.DONE
              
           if (salsu == 0 and emailt == 0):
              p = find_element(dom, "ilmoitus", "p")
              teksti = "Käyttäjätunnusta ei löytynyt"
          
              text = dom.createTextNode(teksti.decode("UTF-8"))
              p.appendChild(text)
              req.write(dom.toxml('UTF-8'))
              return apache.DONE      
           else:
              req.write(dom.toxml('UTF-8'))
              return apache.DONE
        else:
            req.write(dom.toxml('UTF-8'))
            return apache.DONE     

               
# Etsii elementit html-tiedostosta   
def find_element(root, id, element="*"):
    for e in root.getElementsByTagName(element):
      if e.hasAttribute("id") and e.getAttribute("id") == id:
         return e
    return None          
  