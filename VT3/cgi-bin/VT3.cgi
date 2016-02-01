#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, cgitb

print """Content-type: text/html

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"/>
<title>Ruudukko</title>
<link rel="StyleSheet" href="tyylit.css" type="text/css"/>
</head>
<body>

<h1>Ruudukko</h1>

<p>Kerro luotavan shakkiruudukon koko. Ruudukko on yhtä monta ruutua
leveä kuin korkea. </p>

<form method="get">
<fieldset>
<p><label>Leveys <input type="text" name="x" /></label></p>
<p><label>Teksti <input type="text" name="teksti" /></label></p>
</fieldset>
<p><input type="submit" value="Luo" /></p>
</form>
<table>
"""

form = cgi.FieldStorage()
luku = int(form.getvalue('x'))
teksti = form.getvalue('teksti')
if teksti is not None:
   teksti2 = cgi.escape(teksti);
if teksti is None: teksti2 = ""

if luku > 5:
   if luku < 13:
      for x in xrange(1, luku + 1):
          print "<tr>"
          for y in xrange(1, luku + 1):
			 if ((y % 2 == 1) & (x % 2 == 1)): 
			    print "<td class='musta'>" + teksti2 + "</td>"
			 elif ((y % 2 == 0) & (x % 2 == 0)):
			    print "<td class='musta'>" + teksti2 + "</td>"
			 else: 
			    print "<td>" + teksti2 + "</td>"   
			 if (y >= luku): 
			    print "</tr>"
                

print """
</table>
</body>
</html>
"""
