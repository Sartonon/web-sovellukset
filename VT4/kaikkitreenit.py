# -*- coding: UTF-8 -*-
from xml.dom.minidom import getDOMImplementation, parse, parseString
import os
from pysqlite2 import dbapi2 as sqlite
import sys

def index(req):
   req.content_type = 'text/html ;charset=utf-8'
   con = sqlite.connect( '/nashome3/sajukaru/html/hidden/kanta/kanta')
   con.text_factory = unicode
   con.row_factory = sqlite.Row
   
   nimi = req.session["nimi"]
   
   # Etsitään kaikki treenit ja järjestetään nimen ja alkuajan mukaan
   sql = """
   SELECT *
   FROM Treeni, Henkilo
   WHERE Treeni.Email = Henkilo.Email
   ORDER BY Henkilo.Etunimi, Treeni.Alkuaika
   """
   tunnus = req.session["kayttaja"]
   cur = con.cursor()
   try:
      cur.execute(sql)
   except: 
      # vaatii koodin alkuun rivin: import sys
      req.write("nyt tuli virhe: %s" % sys.exc_info()[0])
   
   
   pohja = os.path.join(os.path.dirname(req.filename), 'kaikkitreenit.html')
   dom = parse(pohja)
   
   valikko = find_element(dom, "valikko", "ul")
   li = dom.createElement("li")
   nimi1 = dom.createTextNode(nimi)
   li.appendChild(nimi1)
   valikko.appendChild(li)
   
   
   body = dom.getElementsByTagName("body")
   i = 1
   # Listataan kaikki minidom-rajapinnan kautta
   for rivi in cur:
     etunimi = rivi["Etunimi"]
     sukunimi = rivi["Sukunimi"]
     h3 = dom.createElement("h3")
     text = dom.createTextNode(etunimi + " " + sukunimi)
     i = i + 1
     ul = dom.createElement("ul")
     h3.appendChild(text)
     body[0].appendChild(h3)
     body[0].appendChild(ul)
     li = dom.createElement("li")
     ul.appendChild(li)
     text = dom.createTextNode("Alkuaika: " + str(rivi["Alkuaika"]))
     li.appendChild(text)
     
     li = dom.createElement("li")
     ul.appendChild(li)
     text = dom.createTextNode("Kesto: " + str(rivi["kesto"]))
     li.appendChild(text)
     
     li = dom.createElement("li")
     ul.appendChild(li)
     text = dom.createTextNode("Kilometrit: " + str(rivi["Km"]))
     li.appendChild(text)
       
     li = dom.createElement("li")
     ul.appendChild(li)
     text = dom.createTextNode("Keskisyke: " + str(rivi["Syke_avg"]))
     li.appendChild(text) 

     li = dom.createElement("li")
     ul.appendChild(li)
     text = dom.createTextNode("Maksimisyke: " + str(rivi["Syke_max"]))
     li.appendChild(text) 

     li = dom.createElement("li")
     ul.appendChild(li)
     text = dom.createTextNode("Kalorit: " + str(rivi["Kalorit"]))
     li.appendChild(text)

     li = dom.createElement("li")
     ul.appendChild(li)
     teksti = rivi["Kommentti"]
     
     #teksti1 = teksti.decode("UTF-8")
     if teksti is not None:
       text = dom.createTextNode("Kommentti: " + teksti)
       li.appendChild(text)         
   
   return dom.toxml('UTF-8')


# Etsii elementin id:n perusteella.
def find_element(root, id, element="*"):
    for e in root.getElementsByTagName(element):
      if e.hasAttribute("id") and e.getAttribute("id") == id:
         return e
    return None   
   