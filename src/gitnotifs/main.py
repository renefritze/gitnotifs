# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 21:46:35 2012

@author: r_milk01
"""
from configparser import ConfigParser
import jinja2
from datetime import datetime

from gitnotifs import (mail, irc, xmpp)

def format_message(rows, cfg):
    header_tpl = jinja2.Template(cfg['message.header'])
    body_tpl = jinja2.Template(cfg['message.body'])
    date = datetime.now()
    for (old, new, rev) in rows:
        pass
    return (header_tpl.format(blalh), body_tpl(fprmat))

def notify_rows(rows, config_file):
    cfg = ConfigParser(config_file)
    do_mail = cfg.has_section('mail')
    do_irc = cfg.has_section('irc')
    do_xmpp = cfg.has_section('xmpp')
    header, body = format_message(rows, cfg)
    if do_mail:
        mail.notify(header, body, cfg)
    if do_irc:
        irc.notify(header, body, cfg)
    if do_xmpp:
        xmpp.notify(header, body, cfg)
        
