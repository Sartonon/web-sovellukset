# -*- coding: UTF-8 -*-
from xml.dom.minidom import getDOMImplementation, parse, parseString
import os
from pysqlite2 import dbapi2 as sqlite
import sys
import cgi

def index(req):
   req.content_type = 'text/html ;charset=utf-8'
   
   con = sqlite.connect( '/nashome3/sajukaru/html/hidden/kanta/kanta')
   
   con.text_factory = str
   con.row_factory = sqlite.Row
   nimi = req.session["nimi"]
   tunnus = req.session["kayttaja"]
   pohja = os.path.join(os.path.dirname(req.filename), 'lisaatreeni1.html')
   dom = parse(pohja)
   
   form = find_element(dom, "form", "form")
   form.setAttribute("action", req.uri)
   treeniid = 0
   treenityyppiid = 0
   lajityyppiid = 0
   
   # Treenien helppo poisto nappulasta
   if req.form.getfirst("poista") == "Poista treenit":
     sql = """
     DELETE FROM Treeni
     WHERE Treeni.Email = :tunnus
     """
     cur = con.cursor()
     try:
       cur.execute(sql, {"tunnus":tunnus})
       con.commit()      
     except:
       req.write(str(sys.exc_info()[0]))
       req.write(str(sys.exc_info()[1]))
       req.write(str(sys.exc_info()[2]))
       virheilmoitus(dom)
   
   # Laitetaan syötetyt tiedot tietokantaan
   if req.form.getfirst("lisaa") == "Lisää treeni":
     cur = con.cursor()
     sql = """
     INSERT INTO Treeni (Alkuaika, kesto, Km, Syke_avg, Syke_max, Kalorit, Kommentti, Email)
     VALUES (:alkuaika, :kesto, :Km, :syke_avg, :syke_max, :kalorit, :kommentti, :email)
     """
     
     # Tarkistetaan onko tiedot syötetty oikeassa muodossa
     try:
       alkuaika = str(req.form.getfirst("alkuluku"))
       kesto = req.form.getfirst("kesto")
       km = int(req.form.getfirst("km"))
       syke_avg = int(req.form.getfirst("keskisyke"))
       syke_max = int(req.form.getfirst("sykemax"))
       kalorit = int(req.form.getfirst("kalorit"))
       kommentti = str(req.form.getfirst("kommentti", " "))
       #kommentti = kommentti.decode("UTF-8")
       cur.execute(sql, {"alkuaika":alkuaika, "kesto":kesto,
                         "Km":km, "syke_avg":syke_avg, "syke_max":syke_max, "kalorit":kalorit,
                          "kommentti":kommentti, "email":tunnus})
          
       #req.write(str(id))
       #con.commit()
       treeniid = cur.lastrowid

       # Selvitetään mikä on valitun treenityypin ID       
       sql = """
       SELECT *
       FROM Treenityyppi
       """
     
       #select = find_element(dom, "treenit", "select")
       cur.execute(sql)
       
       #id = 0     
       #Selvitetään valittu treenityyppi alasvetovalikosta
       i = 1
       for rivi in cur:
         if req.form.getfirst("treenit") == str(i):
             treenityyppiid = i
            
         i = i + 1         
       # Ja lisätään oikeat ID:t kantaan
       
       
       
       sql = """
       SELECT *
       FROM Laji
       """
       
       #select = find_element(dom, "lajit", "select")
       cur.execute(sql)
       
       # Etsitään valittu laji alasvetovalikosta     
       i = 1
       for rivi in cur:
         if req.form.getfirst("lajit") == str(i):
             lajityyppiid = i            
         i = i + 1
       
       # Ja asetetaan tietokantaan
       sql = """
       INSERT INTO lajia (TreeniID, LajiID)
       VALUES (:treeniid, :lajityyppiid)
       """
       
       cur.execute(sql, {"treeniid":treeniid, "lajityyppiid":lajityyppiid})
       
       # Kommitoidaan ja ilmoitetaan että lisäys onnistui
       con.commit()
       
       body = dom.getElementsByTagName("body")
       p = dom.createElement("p")
       teksti = "Treenin lisäys onnistui!"
       
       text = dom.createTextNode(teksti.decode("UTF-8"))
       
       p.appendChild(text)
       body[0].appendChild(p)       
     except:
        #req.write(str(sys.exc_info()[0]) + "\n")
        #req.write(str(sys.exc_info()[1]) + "\n")
        #req.write(str(sys.exc_info()[2]) + "\n")
        virheilmoitus(dom)
     
   
   
   
   sql = """
   SELECT Treenityyppinimi
   FROM Treenityyppi
   """
   cur = con.cursor()
   try:
      cur.execute(sql)
   except: 
      # vaatii koodin alkuun rivin: import sys
      #req.write("nyt tuli virhe: %s" % sys.exc_info()[0])
      body = dom.getElementsByTagName("body")
      p = dom.createElement("p")
      text = dom.createTextNode("Jokin meni pieleen, tietoja ei tallennettu")
      p.appendChild(text)
      body[0].appendChild(p)
   
   valikko = find_element(dom, "valikko", "ul")
   li = dom.createElement("li")
   nimi1 = dom.createTextNode(nimi)
   li.appendChild(nimi1)
   valikko.appendChild(li)

   
   i = 1
   select = find_element(dom, "treenit", "select")
   for rivi in cur:
        
     option = dom.createElement("option")
     teksti = rivi["Treenityyppinimi"].decode("UTF-8")
     option.setAttribute("value", str(i))
     text = dom.createTextNode(teksti)
     option.appendChild(text)
     select.appendChild(option)
     i = i + 1
   
   sql = """
   SELECT Lajinimi
   FROM Laji
   """
   cur = con.cursor()
   try:
      cur.execute(sql)
   except: 
      # vaatii koodin alkuun rivin: import sys
      #req.write("nyt tuli virhe: %s" % sys.exc_info()[0])
      virheilmoitus(dom)
      
   i = 1
   select = find_element(dom, "lajit", "select")
   for rivi in cur:
     option = dom.createElement("option")
     teksti = rivi["Lajinimi"].decode("UTF-8")
     option.setAttribute("value", str(i))
     text = dom.createTextNode(teksti)
     option.appendChild(text)
     select.appendChild(option)
     i = i + 1
   
   return dom.toxml('UTF-8')
   

# Etsii elementit html-tiedostosta   
def find_element(root, id, element="*"):
    for e in root.getElementsByTagName(element):
      if e.hasAttribute("id") and e.getAttribute("id") == id:
         return e
    return None 
    
def virheilmoitus(dom):
   body = dom.getElementsByTagName("body")
   p = dom.createElement("p")
   text = dom.createTextNode("Jokin meni pieleen, tietoja ei tallennettu")
   p.appendChild(text)
   body[0].appendChild(p)