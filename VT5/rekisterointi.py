from mod_python import apache
from pysqlite2 import dbapi2 as sqlite
import os
import sys
import sha

def index(req):
    # Uuden käyttäjän luominen
    con = sqlite.connect('/nashome3/sajukaru/html/hidden/kanta/kanta')
    con.text_factory = unicode
    con.row_factory = sqlite.Row
    req.content_type = "text/plain; charset=UTF-8"
    #time.sleep(1)
    etunimi = req.form.getfirst("etunimi")
    sukunimi = req.form.getfirst("sukunimi")
    tunnus = req.form.getfirst("uusitunnus")
    salasana = req.form.getfirst("uusisalasana")
    
    hash = sha.new()
    hash.update(tunnus)
    hash.update(salasana)
    salasana1 = hash.hexdigest()
    
    km = req.form.getfirst("km")
    
    sql = """
          INSERT INTO Henkilo (Email, Salasana, Etunimi, Sukunimi)
          VALUES (:tunnus, :salasana, :etunimi, :sukunimi)
    """
    
    cur = con.cursor()
    try:
       cur.execute(sql, {"tunnus":tunnus, "salasana": salasana1, "etunimi": etunimi, "sukunimi": sukunimi})
       con.commit()
       req.write("ok")
    except: 
       # vaatii koodin alkuun rivin: import sys
       req.write("nyt tuli virhe: %s" % sys.exc_info()[0])
       
    return   