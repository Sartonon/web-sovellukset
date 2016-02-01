from gluon.contrib.login_methods.gae_google_account import GaeGoogleAccount
auth.settings.login_form = GaeGoogleAccount()
import sys
import datetime
now = datetime.datetime.now()




db.define_table('laji',
  Field("lajinimi", 'string', required=True))
  
db.define_table('treenityyppi',
  Field("treenityyppinimi", 'string', required=True))
  

# oman tietokannan määrittelyt käyttäen web2pyn DAL-rajapintaa
db.define_table('treeni', 
  Field('laji', 'reference laji', required=False),
  Field('treenityyppi', 'list:reference treenityyppi', required=False),
  Field('alkuaika', 'datetime', required=True),
  Field('kesto', 'time', required=True, label="Kesto"),
  Field('km', 'integer', required=False, label="Kilometrit"),
  Field('syke_avg', 'integer', required=False, label="Keskisyke"),
  Field('syke_max', 'integer', required=False, label="Maksimisyke"),
  Field('kalorit', 'integer', required=False, label="Kalorit"),
  Field('kommentti', 'text', required=False, label="Kommentti"),
  Field('treenaaja', 'reference auth_user', required=True))
  

# Tietokannan määrityksiä
  
db.treeni.laji.requires = IS_IN_DB(db, db.laji.id, '%(lajinimi)s')
db.treeni.treenityyppi.requires = IS_IN_DB(db, db.treenityyppi.id, '%(treenityyppinimi)s', multiple=True)
db.treeni.treenityyppi.widget = SQLFORM.widgets.checkboxes.widget

db.treeni.km.requires = IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0, sys.maxint, error_message='Ei saa olla negatiivinen luku'))
db.treeni.syke_avg.requires = IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0, sys.maxint, error_message='Ei saa olla negatiivinen luku'))
db.treeni.syke_max.requires = IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0, sys.maxint, error_message='Ei saa olla negatiivinen luku'))
db.treeni.kalorit.requires = IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0, sys.maxint, error_message='Ei saa olla negatiivinen luku'))

db.treeni.alkuaika.requires = IS_DATETIME_IN_RANGE(format=T('%Y-%m-%d %H:%M:%S'),
                       maximum=datetime.datetime.now(),
                       error_message='Aika ei saa olla tulevaisuudessa!')

db.treeni.treenaaja.writable = db.treeni.treenaaja.readable = False
db.treenityyppi.treenityyppinimi.requires = [IS_LOWER(), IS_NOT_IN_DB(db, 'treenityyppi.treenityyppinimi', error_message='Treenityyppi on jo lisätty!')]
db.laji.lajinimi.requires = [IS_LOWER() ,IS_NOT_IN_DB(db, 'laji.lajinimi', error_message='Laji on jo lisätty!')]