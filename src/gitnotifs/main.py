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
            self.filename = '%s --> %s' % (d.a_blob.path, d.b_blob.path)
        else:
            self.cat = 'changed'
            self.filename =  d.a_blob.path
        self.diff = d.diff

def _get_diffs(old_rev, new_rev, rev_name, cfg):
    repo = git.Repo(cfg['general.repo_path'])
    commits = list(repo.iter_commits('%s..%s' %(old_rev,new_rev)))
    change_types = [[d.iter_change_type(t) for t in DiffIndex.change_type] 
                    for d in [c.parents[0].diff(c, create_patch=True) for c in commits]]
    def _diffs():
        for d in change_types:
            for k in d:
                for j in k:
                    yield j    
    return [FileDiff(d) for d in _diffs()] 
        
def format_message(module, diffs, old_rev, new_rev, rev_name, cfg):
    try:
        header_tpl = jinja2.Template(cfg['%s.header'%module])
        body_tpl = jinja2.Template(cfg['%s.body'%module])
    except NoOptionError as e:
        header_tpl = jinja2.Template(cfg['general.header'])
        body_tpl = jinja2.Template(cfg['general.body'])
    date = datetime.now()
    
    return header_tpl.render(locals()), body_tpl.render(locals())

def notify(old_rev, new_rev, rev_name, config_file):
    cfg = Config()
    cfg.read([config_file, os.path.expanduser('~/.gitnotifs')])
    diffs = _get_diffs(old_rev, new_rev, rev_name, cfg)
    for transport in cfg['general.active'].split():
        pname = 'gitnotifs.%s' % transport
        __import__(pname)
        module  = sys.modules[pname]
        header, body = format_message(transport, diffs, old_rev, new_rev, rev_name, cfg)
        print header
        print body 
        module.notify(header, body, cfg)
        
#read oldrev newrev refname
#
#branch=$(echo $refname | sed "s;refs/heads/;branch: ;g")
#repo=$(echo ${PWD} | sed "s;^\(.*\)/\(.*\)/\(.*\)$;\2/\3;g")
#echo "notifying of commits"
##project=${repo%.git}
#project=${repo}
#url=http://dune-project.uni-muenster.de/cgit/${project}/commit/?id=${newrev}
#jabnotif "$(git log --shortstat --pretty=format:"${repo}, $branch%n%cn: %s%n%b" $oldrev..$newrev) ${url}" $(cat notifs) &> /dev/null
