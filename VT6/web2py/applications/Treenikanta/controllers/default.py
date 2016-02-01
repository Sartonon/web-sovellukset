# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

response.menu=[['TIEA218', True,'http://appro.mit.jyu.fi/web-sovellukset/'],
    ['Treenilistaus', False, URL('listaus')], ['Lisää treeni', False, URL('treeni')],
    ['Lisää laji', False, URL('lisaalaji')], ['Lisää treenityyppi', False, URL('treenityyppi')]]

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))

@auth.requires_login()   
def treeni():
    user = db.auth_user(auth.user.id)
    if request.get_vars['id'] != None:
        treeni = db.treeni( request.get_vars['id'] )
        form = SQLFORM(db.treeni, treeni, deletable=True)
    else:
        form = SQLFORM(db.treeni)
    form.vars.treenaaja = auth.user.id 
    if form.process().accepted:
       response.flash = 'Treeni on lisätty'
    elif form.errors:
       response.flash = 'Lomakkeen tiedoissa on virheitä'
    else:
       response.flash = 'Täytä lomake lisätäksesi uuden treenin'
    return dict (lomake=form)   

@auth.requires_login()    
def lisaalaji():
    form = SQLFORM(db.laji)
    if form.process().accepted:
       response.flash = 'Laji on lisätty'
    elif form.errors:
       response.flash = 'Lomakkeen tiedoissa on virheitä'
    else:
       response.flash = 'Täytä lomake lisätäksesi uuden lajin'
    return dict (lomake=form)

@auth.requires_login()    
def treenityyppi():
    form = SQLFORM(db.treenityyppi)
    if form.process().accepted:
       response.flash = 'Treenityyppi on lisätty'
    elif form.errors:
       response.flash = 'Lomakkeen tiedoissa on virheitä'
    else:
       response.flash = 'Täytä lomake lisätäksesi uuden treenityypin'
    return dict (lomake=form)


# Listaa treenit (ei vaadi kirjautumista)   
def listaus():
    try:
      user = db.auth_user(auth.user.id)
    except:
      user = ""    
    treenit = db().select(db.treeni.ALL, orderby=db.treeni.treenaaja)
    lajit = {}
    treenaajat = {}
    treenityypit = {}
    if request.get_vars['id'] != None:
        treeni = db.treeni( request.get_vars['id'] )
        form = SQLFORM(db.treeni, treeni, deletable=True, showid=False)
    else:
       form = ""
    if form != "":   
       if form.process().accepted:
          response.flash = 'Treeniä muokattu'
          return redirect(URL('listaus'))
       elif form.errors:
          response.flash = 'Treenin tiedoissa virheitä'
       else:
          response.flash = 'Täytä lomaketta'
    
    # Haetaan lajit treeniä kohden
    for item in treenit:
       try:
         laji = db(db.laji.id == item.laji).select(db.laji.ALL).first()
         lajit[item.id] = laji.lajinimi
       except:
         lajit[item.id] = "" 
    for item in treenit:
       try:
         treenaaja = db(db.auth_user.id == item.treenaaja).select(db.auth_user.ALL).first()
         treenaajat[item.id] = treenaaja.first_name + " " + treenaaja.last_name
       except:
         treenaajat[item.id] = ""
    
    # Haetaan treeniin kuuluva treenityypit
    for item in treenit:
      treenityypit[item.id] = []
      try:
       for tyyppi in item.treenityyppi:
          treenityyp = db(db.treenityyppi.id == tyyppi).select(db.treenityyppi.ALL).first()
          treenityypit[item.id].append( treenityyp.treenityyppinimi)
      except:
        treenityypit[item.id] = ""   
       #try:
      #   treenityyppi = db(db.treenityyppi.id == item.treenityyppi).select(db.treenityyppi.ALL)
      #   for treeni in treenityyppi:
     #      treenityypit[treeni.id] = treeni.treenityyppinimi
      # except:
     #    treenityypit[item.id] = ""
         
    return dict (treenit=treenit, lajit=lajit, treenaajat=treenaajat, lomake=form, user=user, treenityypit=treenityypit)
    
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
