import xmpp
import time

def notify(header, body, cfg):
    to_jids=cfg['jabber.recipients'].split()
    text=header + '\n' + body  
    my_jid=xmpp.protocol.JID(cfg['jabber.jid'])
    cl=xmpp.Client(my_jid.getDomain(),debug=[])
    con=cl.connect()
    if not con:
        raise Exception('could not connect!')       
    auth=cl.auth(my_jid.getNode(),cfg['jabber.pw'],resource=my_jid.getResource())
    if not auth:
        raise Exception('could not authenticate!')
    for jid in to_jids:
            cl.send(xmpp.protocol.Message(to=jid,body=text,typ='chat'))
            time.sleep(1)   # some older servers will not send the message if you disconnect immediately after sending
    cl.disconnect()
