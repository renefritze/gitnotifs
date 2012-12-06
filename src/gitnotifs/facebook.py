import time

import _common_xmpp


def notify(header, body, cfg, link):
    to_names=[n.strip() for n in cfg['facebook.recipients'].split('\n')]
    print to_names
    cl = _common_xmpp.get_client('facebook', header, body, cfg)
    roster = cl.getRoster()

        #to_raw_jids 
    for jid in [r for r in roster.keys() if roster.getName(r) in to_names]:
        _common_xmpp.send(cl, header, body, jid)
        time.sleep(4)   # some older servers will not send the message if you disconnect immediately after sending
    cl.disconnect()