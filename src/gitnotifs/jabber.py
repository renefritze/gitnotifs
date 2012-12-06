import time

import _common_xmpp


def notify(header, body, cfg, link):
    to_jids=cfg['jabber.recipients'].split('\n')
    cl = _common_xmpp.get_client('jabber', header, body, cfg)
    for jid in to_jids:
        _common_xmpp.send(cl, header, body, jid)
    time.sleep(1)   # some older servers will not send the message if you disconnect immediately after sending
    cl.disconnect()
