# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 21:46:35 2012

@author: r_milk01
"""
from ConfigParser import (RawConfigParser as ConfigParser, NoOptionError)
import jinja2
from datetime import datetime
import sys
import git
import os
import logging
import itertools
from git import DiffIndex

class Config(ConfigParser):
    
    def __getitem__(self, key):
        section, key = key.split('.')
        return self.get(section, key)

class FileDiff(object):
    def __init__(self, diff_index):
        d = diff_index
        if d.new_file:
            self.cat = 'new'
            self.filename = d.b_blob.path
        elif d.deleted_file:
            self.cat = 'deleted'
            self.filename = d.a_blob.path
        elif d.renamed:
            self.cat = 'renamed'
            self.filename = '%s --> %s' % (d.rename_from, d.rename_to)
        else:
            self.cat = 'changed'
            self.filename =  d.a_blob.path
        self.diff = d.diff

def _get_diffs(old_rev, new_rev, rev_name, cfg):
    repo = git.Repo(cfg['general.repo_path'])
    commits = list(repo.iter_commits('%s..%s' %(old_rev,new_rev)))
    changes = [[d.iter_change_type(t) for t in DiffIndex.change_type] 
                    for d in [c.parents[0].diff(c, create_patch=True) for c in commits]]
    chain_iter = itertools.chain.from_iterable
    diffs = [FileDiff(d) for d in chain_iter(chain_iter([d for d in changes]))]
    return diffs, commits
        
def format_message(module, diffs, commits, old_rev, new_rev, rev_name, cfg):
    branch = rev_name.split('/')[-1]
    project = os.path.basename(cfg['general.repo_path'])
    counts = dict()
    for i in ['new', 'deleted', 'renamed', 'changed']:
        counts[i] = len([f for f in diffs if f.cat == i])
    statstring = ' | '.join(['%d %s'%(u, h) for h,u in counts.iteritems()])
    try:
        header_tpl = jinja2.Template(cfg['%s.header'%module])
    except NoOptionError as e:
        header_tpl = jinja2.Template(cfg['general.header'])
    try:
        body_tpl = jinja2.Template(cfg['%s.body'%module])
    except NoOptionError as f:
        body_tpl = jinja2.Template(cfg['general.body'])
    date = datetime.now()
    return header_tpl.render(locals()), body_tpl.render(locals())

def notify(old_rev, new_rev, rev_name, config_file=None):
    cfg = Config()
    used = cfg.read([os.path.expanduser('~/.gitnotifs'), config_file])
    logging.debug('using %s as config'%used)
    diffs, commits = _get_diffs(old_rev, new_rev, rev_name, cfg)
    for transport in cfg['general.active'].split():
        pname = 'gitnotifs.%s' % transport
        logging.info('module: %s' % pname)
        __import__(pname)
        module  = sys.modules[pname]
        header, body = format_message(transport, diffs, commits, old_rev, new_rev, rev_name, cfg)
        module.notify(header, body, cfg)
        
