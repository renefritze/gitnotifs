import xmpp

def get_client(module, header, body, cfg):
    my_jid=xmpp.protocol.JID(cfg['%s.jid'%module])
    cl=xmpp.Client(my_jid.getDomain(),debug=[])
    con=cl.connect()
    if not con:
        raise Exception('could not connect!')       
    auth=cl.auth(my_jid.getNode(),cfg['%s.pw'%module],resource=my_jid.getResource())
    if not auth:
        raise Exception('could not authenticate!')
    return cl

def send(client, header, body, jid):
    text=header + '\n' + body  
    client.send(xmpp.protocol.Message(to=jid,body=text,typ='chat'))
