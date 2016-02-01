from mod_python import apache, Session


def handler(req):
        if not hasattr(req, 'session'):
                req.session = Session.Session(req)
        return apache.OK