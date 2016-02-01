from xml.dom.minidom import getDOMImplementation, parse, parseString
import os
from mod_python import util

def index(req):
   req.content_type = 'text/html ;charset=utf-8'
   
   if req.form.getfirst("ulos") == "Kirjaudu ulos":
      req.session.invalidate()
      util.redirect(req, 'http://users.jyu.fi/~sajukaru/Web-Sovellukset/VT4/')
      
   
   pohja = os.path.join(os.path.dirname(req.filename), 'uloskirjaus.html')
   dom = parse(pohja)
   
   return dom.toxml('UTF-8')