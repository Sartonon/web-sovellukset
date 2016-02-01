#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import cgitb
cgitb.enable()
import cgi
import time
import datetime
import random
import os
from xml.dom.minidom import getDOMImplementation, parse, parseString

dom1 = parse("/nashome3/sajukaru/html/cgi-bin/doc.html")

print "Content-type: text/html\n"

table = dom1.createElement("table")
form2 = dom1.getElementsByTagName("form")
body = dom1.getElementsByTagName("body")
fieldset = dom1.getElementsByTagName("fieldset")

form = cgi.FieldStorage()
luku = form.getvalue('x')
teksti = form.getvalue("teksti")

if teksti is not None:
   teksti = cgi.escape(teksti)
   tekstiString = str(form.getvalue("teksti"))
   hidden = dom1.createElement("input")
   hidden.setAttribute("name", "teksti1")
   hidden.setAttribute("value", tekstiString)
   hidden.setAttribute("type", "hidden")
   fieldset[0].appendChild(hidden)   
else:
   teksti = str(form.getvalue("teksti1"))
   hidden = dom1.createElement("input")
   hidden.setAttribute("name", "teksti1")
   hidden.setAttribute("value", teksti)
   hidden.setAttribute("type", "hidden")
   fieldset[0].appendChild(hidden)   
   if teksti is None:
      teksti = ""

if luku is not None:
   try:
      lukuInt = int(form.getvalue('x'))
      koko = lukuInt
      hidden = dom1.createElement("input")
      koko1 = str(luku)
      hidden.setAttribute("name", "ruudukonkoko")
      hidden.setAttribute("value", koko1)
      hidden.setAttribute("type", "hidden")
     # fieldset2 = dom1.createElement("fieldset")
      fieldset[0].appendChild(hidden)
   except ValueError:
       koko = 0
   
   
  # form2[0].appendChild(fieldset2)
 # fieldset2.appendChild(hidden)


if luku is None:
   koko = form.getvalue('ruudukonkoko')
   
   if koko is None:
      koko = 0
   
  # fieldset2 = dom1.createElement("fieldset")
  # form2[0].appendChild(fieldset2)   
   hidden = dom1.createElement("input")
   koko1 = str(koko)
   hidden.setAttribute("name", "ruudukonkoko")
   hidden.setAttribute("value", koko1)
   hidden.setAttribute("type", "hidden")
  # fieldset2.appendChild(hidden)
   fieldset[0].appendChild(hidden)
   if koko1 is not None:
    koko = int(koko)
   else: koko = 0  
   

lol = form.getvalue("moi")
if lol is not None:
   lol = int(lol)
else:
   lol = 999

if koko != 0:
   form2[0].appendChild(table)
numero = 0



#if luku is not None: 
if (koko < 13 and koko > 5):
   for i in range(1, koko + 1):
      
      tr = dom1.createElement("tr")
      table.appendChild(tr)
      for x in range(1, koko + 1):
         td = dom1.createElement("td")
         
         tr.appendChild(td)
         
         numero = numero + 1
         numero = int(numero)
         if (i < 3 and (numero is not lol)):
            
            numero1 = str(numero)
            button = dom1.createElement("button")
            td.appendChild(button)
            button.setAttribute("class", "blue")
            button.setAttribute("type", "submit")
            button.setAttribute("name" , "moi")
            button.setAttribute("value", numero1)
         if ((i > koko - 2) and (numero != lol)):
            numero1 = str(numero)
            button = dom1.createElement("button")
            td.appendChild(button)
            button.setAttribute("class", "red")
            button.setAttribute("type", "submit")
            button.setAttribute("name" , "moi")
            button.setAttribute("value", numero1)
         if (i >= 3 and i < koko - 1):
            p = dom1.createElement("p")
            teksti1 = dom1.createTextNode(teksti)
            p.appendChild(teksti1)
            td.appendChild(p)      
         if ((x % 2 == 1) & (i % 2 == 1)):
            td.setAttribute("class", "musta")
         elif ((x % 2 == 0) & (i % 2 == 0)):
            tr.appendChild(td)
            td.setAttribute("class", "musta")
         else:
            tr.appendChild(td)



print dom1.toxml('ISO-8859-1') 