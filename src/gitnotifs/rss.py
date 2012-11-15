try:
    import cPickle as pickle
except:
    import pickle

from webhelpers.feedgenerator import Rss201rev2Feed
from datetime import datetime

class Item(object):
    def __init__(self, t, l, a, d):
        self.title = t
        self.link = l
        self.author_name = a
        self.pubdate = datetime.now() 
        self.description = d
    
def notify(header, body, cfg):
    fn = cfg['rss.file']
    pickle_fn = fn + '.pickle'
    try:
        previous = pickle.load(pickle_fn)
    except:
        previous = []
    feed = Rss201rev2Feed(
            title=cfg['rss.title'],
            link='',
            description=cfg['rss.description'],
            language=u"en",
        )
    previous.append(Item(header, '', 'author', body))
    for item in previous:
        feed.add_item(title=item.title, description=item.description, link=item.link, author_name=item.author_name,
                       pubdate=item.pubdate)

    with open(cfg['rss.file'], 'wb') as out:
        feed.write(out, 'utf-8')