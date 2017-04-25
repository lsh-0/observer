#from . import models
from feedgen.feed import FeedGenerator
import logging

LOG = logging.getLogger(__name__)

try:
    import utils
except ImportError:
    from . import utils

def set_obj_attrs(obj, data):
    def set(obj, key, val):
        if ':' in key:
            # namespaced setter, assumes ns has been loaded
            ns, key = key.split(':', 1)
            obj = getattr(obj, ns)
        setter = getattr(obj, key)
        if isinstance(val, list):
            for row in val:
                setter(row)
        else:
            getattr(obj, key)(val)
    [set(obj, key, val) for key, val in data.items()]

def mkfeed(report):
    fg = FeedGenerator()
    fg.load_extension('dc', atom=True, rss=True)

    # extract the report bits
    data = utils.subdict(report, ['id', 'title', 'description', 'link'])

    # rename some bits
    # data = utils.rename(data, [('owner', 'author')]) # for example

    # wrangle some more bits
    data['link'] = {'href': 'https://elifesciences.org', 'rel': 'self'}

    # add some defaults
    data['language'] = 'en'
    data['generator'] = 'observer (using python-feedgen)'

    # set the attributes
    # http://lkiesow.github.io/python-feedgen/#create-a-feed
    set_obj_attrs(fg, data)

    return fg

def add_entry(fg, item):
    entry = fg.add_entry()
    set_obj_attrs(entry, item)
    return entry

def add_many_entries(fg, item_list):
    [add_entry(fg, item) for item in utils.take(250, item_list)]


#
#
#

def article_to_rss_entry(art):
    "coerce a models.Article object to something suitable for the feedgen entry model"
    item = utils.to_dict(art)

    # extract the entry bits
    item = utils.subdict(item, ['id', 'doi', 'title', 'abstract', 'datetime_published'])  # , 'description', 'author', 'category', 'guid', 'pubdate'])

    # rename some bits
    utils.renkeys(item, [
        ('doi', 'link'),
        ('abstract', 'description'),
        ('datetime_published', 'pubdate'),
    ])

    # wrangle
    item['id'] = "https://dx.doi.org/" + item['link']
    item['link'] = {'href': "https://beta.elifesciences.org/articles/" + utils.pad_msid(art.msid)}
    item['author'] = [{'name': a.name, 'email': art.author_email} for a in art.authors.all()]
    item['category'] = [{'term': c.name, 'label': c.label} for c in art.subjects.all()]
    item['dc:dc_date'] = utils.ymdhms(item['pubdate'])
    return item

def format_report(report, context):
    try:
        report.update(context) # yes, this nukes any conflicting keys in the report
        report['title'] = 'eLife: ' + report['title']
        feed = mkfeed(report)
        add_many_entries(feed, map(article_to_rss_entry, report['items'])) # deliberate use of lazy map
        return feed.rss_str(pretty=True).decode('utf-8')
    except BaseException as e:
        LOG.exception("unhandled exception formatting report %r", report)
        raise

#
#
#

if __name__ == '__main__':
    demo_report = {
        'title': 'a demonstration',
        'id': 'data.elifesciences.org/latest.rss',
        'description': 'this is a simple asdf'
    }
    entry = {
        'title': 'item title',
        'link': {'href': 'some id'},
        'dc:dc_date': '2017-01-01',
        'category': [
            {'term': 'foo', 'label': 'Foo'},
            {'term': 'foo', 'label': 'Foo'}
        ]
    }

    feed = mkfeed(demo_report)
    add_entry(feed, entry)
    #entryobj = add_entry(feed, entry)
    # entryobj.dc.dc_date('2017-01-01')
    print(feed.rss_str(pretty=True).decode('utf8'))