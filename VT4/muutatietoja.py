# -*- coding: UTF-8 -*-
import os
from pysqlite2 import dbapi2 as sqlite
import sys
import sha


def index(req):
   req.content_type = 'text/html ;charset=utf-8'
   
   con = sqlite.connect( '/nashome3/sajukaru/html/hidden/kanta/kanta')
   con.text_factory = str
   con.row_factory = sqlite.Row
   email = req.session["kayttaja"]
   nimi = req.session["nimi"]
   nimihaku = """SELECT Etunimi, Sukunimi
                 FROM Henkilo
                 WHERE Henkilo.Email = :email"""
      
   if req.form.getfirst("muuta") == "Muuta tietoja":
      uusikayttajatunnus = str(req.form.getfirst("kayttajatunnus", "tyhja"))
      uusisalasana = str(req.form.getfirst("salasana", "tyhja"))
      uusikayttajanimi = str(req.form.getfirst("nimi", "tyhja"))
      uusikayttajasukunimi = str(req.form.getfirst("sukunimi", "tyhja"))
      
      sql = """UPDATE Henkilo SET Etunimi = :uusinimi WHERE Email = :email"""
      sql2 = """UPDATE Henkilo SET Sukunimi = :uusisukunimi WHERE Email = :email"""
      sql3 = """UPDATE Henkilo SET Email = :uusiemail WHERE Email = :email"""
      sql4 = """UPDATE Henkilo SET Salasana = :uusisalasana WHERE Email = :email"""
      #req.write(uusikayttajanimi)
      cur = con.cursor()
      i = 0
      try:
       if uusikayttajanimi != "":
          cur.execute(sql, {"uusinimi":uusikayttajanimi, "email": email})
          #req.session["nimi"] = uusikayttajanimi.decode("UTF-8")
          #req.session.save()
       if uusikayttajasukunimi != "":
          cur.execute(sql2, {"uusisukunimi":uusikayttajasukunimi, "email": email})
       # Uusi email, päivitetään myös salasanaa   
       if uusikayttajatunnus != "":
          
          
          cur.execute(sql3, {"uusiemail":uusikayttajatunnus, "email": email})
          req.session["kayttaja"] = uusikayttajatunnus
          req.session.save()
          hash = sha.new()
          hash.update(str(uusikayttajatunnus))
          i = i + 1
          if uusisalasana != "": 
             hash.update(str(uusisalasana))
          else:
             hash.update('salasana')
          uusisalasana = hash.hexdigest()
          cur.execute(sql4, {"uusisalasana":uusisalasana, "email":uusikayttajatunnus})
       if uusisalasana != "" and i == 0:
          kayttaja = req.session["kayttaja"]
          #req.write("salasana muutettu")
          hash = sha.new()
          hash.update(kayttaja.decode("UTF-8"))
          hash.update(str(uusisalasana))
          uusisalasana = hash.hexdigest()
          cur.execute(sql4, {"uusisalasana":uusisalasana, "email":kayttaja})         
          
       
       cur = con.cursor()
       try:
          cur.execute(nimihaku, {"email":email})
          for rivi in cur:
            nimi = rivi["Etunimi"] + " " + rivi["Sukunimi"]
            #req.write(nimi)
            req.session["nimi"] = nimi.decode("UTF-8")
            req.session.save()
       except:
         req.write("jokin meni pieleen")
      # body = dom.getElementsByTagName("body")
      # p = dom.createElement("p")
      # teksti = "Onnistui"
      # text = dom.createTextNode(teksti)
      # p.appendChild(p)
      # body[0].appendChild(p)          
      except:
       req.write(str(sys.exc_info()[0]))
       req.write(str(sys.exc_info()[1]))
       req.write(str(sys.exc_info()[2]))
   
      con.commit()
   con.close()
   # EI ole dom-rajapinnan kautta koska tämä kaatoi user.jyu.fi palvelimen :)
   html = """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fi" lang="fi">
<head>
<title>Tietojen muutos</title>
<link rel="StyleSheet" href="tyylit.css" type="text/css"/>
</head>
<body>
<ul id="valikko">
     <li><a href="index.py">Omat treenit</a></li>
     <li><a href="lisaatreeni.py">Lisää treeni</a></li>
     <li><a href="kaikkitreenit.py">Kaikki treenit</a></li>
     <li><a href="ulos.py">Kirjaudu ulos</a></li>
     <li></li>
     
</ul>
<h1>Muuta tietoja:</h1>
<form id="form" action="" method="post">
   <p>
        <label for="kauttajatunnus">Uusi käyttäjätunnus: </label><input type="text" name="kayttajatunnus" id="kayttajatunnus"></input>
      </p>
      <p>
         <label for="salasana">Uusi salasana: </label><input type="text" name="salasana" id="salasana"></input>
      </p>
      <p>
         <label for="nimi">Uusi nimi: </label><input type="text" name="nimi" id="nimi"></input>
      </p>
      <p>
         <label for="sukunimi">Uusi sukunimi: </label><input type="text" name="sukunimi" id="sukunimi"></input>
      </p>
      <p>
         <input type="submit" name="muuta" value="Muuta tietoja"></input>
      </p>
      <p>
      Tyhjät ruudut eivät muutu
      </p>
</form>

</body>
</html>"""
   return html