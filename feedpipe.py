#!/usr/bin/python

import feedparser
import feed.atom as FA
from uuid import uuid4
from datetime import datetime


class FeedPipe(object):
    """ FeedPipe is a tool to mutate feeds; it's your very own Yahoo Pipes.

    `It was originally written in Perl <https://metacpan.org/pod/Feed::Pipe>`_
    by `Vince Veselosky <http://www.control-escape.com/>`_, and ported to
    Python by `Arthur Axel fREW Schmidt <https://blog.afoolishmanifesto.com>`_
    for use on AWS Lambda.

    Args:
        title (str): title of feed; defaults to "Combined Feed"

        id (str): id of feed; defaults to autogenerated uuid

        updated (str of iso8601 datetime): last time feed was updated; defaults
        to current time

    Example::

        import FeedPipe from feedpipe;
        fp = FeedPipe(title => "Mah Bukkit") \\
            .cat('1.xml', '2.rss', '3.atom') \\
            .grep(lambda e: 'lolrus' in e.title.text) \\
            .sort \\
            .head

        print(fp.as_xml())

    .. _entry:

        A few of the most important methods in FeedPipe use entry_ objects.
        Entry objects are `sorta documented
        <http://home.blarg.net/~steveha/pyfeed.html>`_,
        but not really.  Basically they have the following properties:

            * id
            * title
            * updated
            * content
            * link
            * summary
            * published

    Bugs:
        Currently not all of `Atom 1.0
        <http://atomenabled.org/developers/syndication/>`_, which the feeds are
        translated to, is supported.  Specifically the following fields are not
        translated:

            * contributor
            * source
            * rights

        Patches to support them very welcome.

    """
    def __init__(self,
                 title="Combined Feed",
                 id=None,
                 updated=None):
        self.title = title

        if id is None:
            id = 'urn:' + str(uuid4())
        self.id = id

        if updated is None:
            updated = datetime.now().isoformat()
        self.updated = updated

        self.entries = []

    def cat(self, feeds):
        """Adds list of new entry_ objects to the FeedPipe

        .. _feed:

            * Filenames
            * URLs
            * a string containing XML

        Example::

            fp.cat([
                'https://blog.afoolishmanifesto.com/index.xml',
                './foo.xml',
            ])

        Args:
            feeds (List[feed_]): an array of feeds

        Returns:
            self: you know, for chaining!
        """
        for feed in feeds:
            data = feedparser.parse(feed)

            for e in data.entries:
                entry = FA.Entry()
                if 'id' in e:
                    entry.id = e.id

                if 'title' in e:
                    entry.title = e.title

                if 'updated' in e:
                    entry.updated = e.updated

                if 'author' in e:
                    entry.author = FA.Author(e.author)

                if 'content' in e:
                    entry.content = e.content[0].value

                if 'link' in e:
                    link = FA.Link(e.link)
                    entry.link = link

                if 'summary' in e:
                    entry.summary = e.summary

                if 'tags' in e:
                    entry.categories = FA.Collection(
                        FA.Category(tag.term,
                                    scheme=tag.scheme,
                                    label=tag.label)
                        for tag in e.tags)

                if 'published' in e:
                    try:
                        entry.published = e.published
                    except ValueError:
                        entry.published = datetime.strptime(
                            e.published, '%a, %d %b %Y %H:%M:%S %Z'
                        ).isoformat()

                self.entries.append(entry)

        return self

    def grep(self, filter):
        """ Filters the entries in the FeedPipe

        Example::

            fp.grep(lambda e: "Video" not in e.title.text)

        Args:
            filter (callback): callback takes an entry; return value is True if
            entry should be included.

        Returns:
            self: for chaining
        """
        self.entries = [x for x in self.entries if filter(x)]

        return self

    def head(self, length=10):
        """ Truncates feed starting at the beginning

        Example::

            fp.head()

        Args:
            length (int): how many entries to include; defaults to 10

        Returns:
            self: for chaining
        """
        self.entries = self.entries[:length]

        return self

    def map(self, transform):
        """ Transforms entries in the FeedPipe

        Example::

            def fix_title(e):
                e.title = "[STATION] " + e.title.text
                return e

            fp.map(fix_title)

        Args:
            transform (callback): callback takes entry_ and returns it,
            possibly modified
        """
        self.entries = [transform(x) for x in self.entries]

        return self

    def reverse(self):
        """ Reverses the entries in the FeedPipe

        Example::

            fp.reverse()

        Returns:
            self: for chaining
        """
        self.entries.reverse()

        return self

    def _default_key(e):
        if e.updated:
            return e.updated.text
        elif e.published:
            return e.published.text

    def sort(self, cmp=None, key=_default_key, reverse=True):
        """ Sorts the entries in the FeedPipe

        Example::

            fp.sort(key=lambda e: e.title.text)

        Args:
            cmp, key, and reverse; matches the interface of `the sorter
            builtin
            <https://docs.python.org/2/library/functions.html#sorted>`_.
            ``key`` defaults to updated/published and ``reverse`` defaults
            to True, so that the default sort is newest at the beginning.
        """

        self.entries.sort(cmp=cmp, key=key, reverse=reverse)

        return self

    def tail(self, length=10):
        """ Truncates the FeedPipe from the end


        Example::

            fp.tail()

        Args:
            length (int): how many entries to include, starting at the end.
            Defaults to 10.

        Returns:
            self: for chaining
        """
        self.entries = self.entries[len(self.entries) - length:]

        return self

    def as_atom_obj(self):
        """ Object for interacting with XML directly

        Example::

            fp.as_atom_obj()

        Returns:
            `feed.atom.Feed <http://home.blarg.net/~steveha/pyfeed.html>`_.
        """
        feed = FA.Feed()
        feed.generator = 'feedpipe 0.0.1'
        if self.title:
            feed.title = self.title

        if self.id:
            feed.id = self.id

        if self.updated:
            feed.updated = self.updated

        for e in self.entries:
            feed.entries.append(e)

        return feed

    def as_xml(self):
        """ Gets the actual XML

        Example::

            fp.as_xml()

        Returns:
            feed: XML encoded in string
        """
        xmldoc = FA.XMLDoc()
        xmldoc.root_element = self.as_atom_obj()

        return str(xmldoc)

    def count(self):
        """

        Example::

            fp.count()

        Returns:
            int: count of entries in the FeedPipe
        """
        return len(self.entries)
