#!/usr/bin/python

# feedparser.SANITIZE_HTML = 0

import unittest
from feedpipe import FeedPipe

ATOM10 = """
<?xml version="1.0" encoding="utf-8"?> <feed xmlns="http://www.w3.org/2005/Atom"
xml:base="http://example.org/" xml:lang="en"> <title type="text"> Sample Feed
</title> <subtitle type="html"> For documentation &lt;em&gt;only&lt;/em&gt;
</subtitle> <link rel="alternate" type="html" href="/"/> <link rel="self"
type="application/atom+xml" href="http://www.example.org/atom10.xml"/> <rights
type="html"> &lt;p>Copyright 2005, Mark Pilgrim&lt;/p> </rights> <generator
uri="http://example.org/generator/" version="4.0"> Sample Toolkit </generator>
<id>tag:feedparser.org,2005-11-09:/docs/examples/atom10.xml</id>
<updated>2005-11-09T11:56:34Z</updated> <entry> <title>First entry title</title>
<link rel="alternate" href="/entry/3"/> <link rel="related" type="text/html"
href="http://search.example.com/"/> <link rel="via" type="text/html"
href="http://toby.example.com/examples/atom10"/> <link rel="enclosure"
type="video/mpeg4" href="http://www.example.com/movie.mp4" length="42301"/>
<id>tag:feedparser.org,2005-11-09:/docs/examples/atom10.xml:3</id>
<published>2005-11-09T00:23:47Z</published>
<updated>2005-11-09T11:56:34Z</updated> <author> <name>Mark Pilgrim</name>
<uri>http://diveintomark.org/</uri> <email>mark@example.org</email> </author>
<contributor> <name>Joe</name> <url>http://example.org/joe/</url>
<email>joe@example.org</email> </contributor> <contributor> <name>Sam</name>
<url>http://example.org/sam/</url> <email>sam@example.org</email> </contributor>
<summary type="text"> Watch out for nasty tricks </summary> <content
type="xhtml" xml:base="http://example.org/entry/3" xml:lang="en-US"><div
xmlns="http://www.w3.org/1999/xhtml">Watch out for
<span style="background-image:url(javascript:window.location='http://example.org/')">
nasty tricks</span></div> </content> </entry> </feed>
"""  # NOQA

ATOM03 = """
<?xml version="1.0" encoding="utf-8"?> <feed version="0.3" xmlns="http://purl.org/atom/ns#" xml:base="http://example.org/" xml:lang="en"> <title type="text/plain" mode="escaped"> Sample Feed </title> <tagline type="text/html" mode="escaped"> For documentation &lt;em&gt;only&lt;/em&gt; </tagline> <link rel="alternate" type="text/html" href="/"/> <copyright type="text/html" mode="escaped"> &lt;p>Copyright 2004, Mark Pilgrim&lt;/p>&lt; </copyright> <generator url="http://example.org/generator/" version="3.0"> Sample Toolkit </generator> <id>tag:feedparser.org,2004-04-20:/docs/examples/atom03.xml</id> <modified>2004-04-20T11:56:34Z</modified> <info type="application/xhtml+xml" mode="xml"> <div xmlns="http://www.w3.org/1999/xhtml"><p>This is an Atom syndication feed.</p></div> </info> <entry> <title>First entry title</title> <link rel="alternate" type="text/html" href="/entry/3"/> <link rel="service.edit" type="application/atom+xml" title="Atom API entrypoint to edit this entry" href="/api/edit/3"/> <link rel="service.post" type="application/atom+xml" title="Atom API entrypoint to add comments to this entry" href="/api/comment/3"/> <id>tag:feedparser.org,2004-04-20:/docs/examples/atom03.xml:3</id> <created>2004-04-19T07:45:00Z</created> <issued>2004-04-20T00:23:47Z</issued> <modified>2004-04-20T11:56:34Z</modified> <author> <name>Mark Pilgrim</name> <url>http://diveintomark.org/</url> <email>mark@example.org</email> </author> <contributor> <name>Joe</name> <url>http://example.org/joe/</url> <email>joe@example.org</email> </contributor> <contributor> <name>Sam</name> <url>http://example.org/sam/</url> <email>sam@example.org</email> </contributor> <summary type="text/plain" mode="escaped"> Watch out for nasty tricks </summary> <content type="application/xhtml+xml" mode="xml" xml:base="http://example.org/entry/3" xml:lang="en-US"> <div xmlns="http://www.w3.org/1999/xhtml">Watch out for <span style="background-image: url(javascript:window.location='http://example.org/')"> nasty tricks</span></div> </content> </entry> </feed>
"""  # NOQA

RSS20 = """
<?xml version="1.0" encoding="utf-8"?> <rss version="2.0"> <channel> <title>Sample Feed</title> <description>For documentation &lt;em&gt;only&lt;/em&gt;</description> <link>http://example.org/</link> <language>en</language> <copyright>Copyright 2004, Mark Pilgrim</copyright> <managingEditor>editor@example.org</managingEditor> <webMaster>webmaster@example.org</webMaster> <pubDate>Sat, 07 Sep 2002 0:00:01 GMT</pubDate> <category>Examples</category> <generator>Sample Toolkit</generator> <docs>http://feedvalidator.org/docs/rss2.html</docs> <cloud domain="rpc.example.com" port="80" path="/RPC2" registerProcedure="pingMe" protocol="soap"/> <ttl>60</ttl> <image> <url>http://example.org/banner.png</url> <title>Example banner</title> <link>http://example.org/</link> <width>80</width> <height>15</height> </image> <textInput> <title>Search</title> <description>Search this site:</description> <name>q</name> <link>http://example.org/mt/mt-search.cgi</link> </textInput> <item> <title>First entry title</title> <link>http://example.org/item/1</link> <description>Watch out for
&lt;span style="background: url(javascript:window.location='http://example.org/')"&gt;
nasty tricks&lt;/span&gt; </description> <author>mark@example.org</author> <category>Miscellaneous</category> <comments>http://example.org/comments/1</comments> <enclosure url="http://example.org/audio/demo.mp3" length="1069871" type="audio/mpeg"/> <guid>http://example.org/guid/1</guid> <pubDate>Thu, 05 Sep 2002 0:00:01 GMT</pubDate> </item> </channel> </rss>
"""  # NOQA

RSS20_DC = """
<?xml version="1.0" encoding="utf-8"?> <rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:admin="http://webns.net/mvcb/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"> <channel> <title>Sample Feed</title> <link>http://example.org/</link> <description>For documentation only</description> <dc:language>en-us</dc:language> <dc:creator>Mark Pilgrim (mark@example.org)</dc:creator> <dc:rights>Copyright 2004 Mark Pilgrim</dc:rights> <dc:date>2004-06-04T17:40:33-05:00</dc:date> <admin:generatorAgent rdf:resource="http://www.exampletoolkit.org/"/> <admin:errorReportsTo rdf:resource="mailto:mark@example.org"/> <item> <title>First entry title</title> <link>http://example.org/archives/2002/09/04.html#first_of_all</link> <guid isPermaLink="false">1983@example.org</guid> <description> Americans are fat. Smokers are stupid. People who don't speak Perl are irrelevant. </description> <dc:subject>Quotes</dc:subject> <dc:date>2002-09-04T13:54:20-05:00</dc:date> <content:encoded><![CDATA[<cite>Ian Hickson</cite>: <q><a href="http://ln.hixie.ch/?start=1030823786&amp;count=1?>
Americans are fat. Smokers are stupid. People who don't speak Perl are irrelevant.
</a></q> ]]> </content:encoded> </item> </channel> </rss>
"""  # NOQA

RSS10 = """
<?xml version="1.0" encoding="utf-8"?> <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:admin="http://webns.net/mvcb/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:cc="http://web.resource.org/cc/" xmlns="http://purl.org/rss/1.0/"> <channel rdf:about="http://www.example.org/index.rdf"> <title>Sample Feed</title> <link>http://www.example.org/</link> <description>For documentation only</description> <dc:language>en</dc:language> <cc:license rdf:resource="http://web.resource.org/cc/PublicDomain"/> <dc:creator>Mark Pilgrim (mark@example.org)</dc:creator> <dc:date>2004-06-04T17:40:33-05:00</dc:date> <admin:generatorAgent rdf:resource="http://www.exampletoolkit.org/"/> <admin:errorReportsTo rdf:resource="mailto:mark@example.org"/> <items> <rdf:Seq> <rdf:li rdf:resource="http://www.example.org/1" /> </rdf:Seq> </items> </channel> <item rdf:about="http://www.example.org/1"> <title>First entry title</title> <link>http://example.org/archives/2002/09/04.html#first_of_all</link> <description> Americans are fat. Smokers are stupid. People who don't speak Perl are irrelevant. </description> <dc:subject>Quotes</dc:subject> <dc:date>2004-05-30T14:23:54-06:00</dc:date> <content:encoded><![CDATA[<cite>Ian Hickson</cite>: <q><a href="http://ln.hixie.ch/?start=1030823786&count=1">
Americans are fat. Smokers are stupid. People who don't speak Perl are irrelevant.
</a></q>]]> </content:encoded> </item> </rdf:RDF>
"""  # NOQA


class TestBasic(unittest.TestCase):

    def _check_feed(self, fp):
        dom = fp.as_atom_obj()
        self.assertEqual(dom.title.text, 'Combined Feed')
        self.assertEqual(dom.entries[0].title.text, 'First entry title')

    def test_atom10(self):
        self._check_feed(FeedPipe().cat([ATOM10]))

    def test_atom03(self):
        self._check_feed(FeedPipe().cat([ATOM03]))

    def test_rss20(self):
        self._check_feed(FeedPipe().cat([RSS20]))

    def test_rss20_dc(self):
        self._check_feed(FeedPipe().cat([RSS20_DC]))

    def test_rss10(self):
        self._check_feed(FeedPipe().cat([RSS10]))

    def test_count(self):
        self.assertEqual(FeedPipe().cat([ATOM10, RSS10]).count(), 2)

    # not testing the actual XML as this module delegates that elsewhere, but
    # instead verifies return type and at least runs the code
    def test_xml(self):
        self.assertEqual(type(FeedPipe().cat([ATOM10, RSS10]).as_xml()),
                         type("station"))

    def test_tail(self):
        fp = FeedPipe().cat(['tests/eg.xml']).tail(2)
        a = fp.as_atom_obj()
        self.assertEqual(a.entries[0].title.text, 'PID Namespaces in Linux')
        self.assertEqual(a.entries[1].title.text, 'Dream On Dreamer')
        self.assertEqual(fp.count(), 2)

    def test_head(self):
        fp = FeedPipe().cat(['tests/eg.xml']).head(2)
        a = fp.as_atom_obj()
        self.assertEqual(a.entries[0].title.text,
                         'Migrating My Blog from Linode to CloudFront')
        self.assertEqual(a.entries[1].title.text, 'UCSPI')
        self.assertEqual(fp.count(), 2)

    def test_sort(self):
        fp = FeedPipe().cat(['tests/eg.xml']) \
                .sort(key=lambda e: e.title.text, reverse=False)
        a = fp.as_atom_obj()
        self.assertEqual(a.entries[0].title.text,
                         'Announcing cgid')
        self.assertEqual(a.entries[1].title.text,
                         'Checking sudoers with visudo in SaltStack')

        fp.sort()
        a = fp.as_atom_obj()
        self.assertEqual(a.entries[0].title.text,
                         'Migrating My Blog from Linode to CloudFront')
        self.assertEqual(a.entries[1].title.text,
                         'UCSPI')

    def test_reverse(self):
        fp = FeedPipe().cat(['tests/eg.xml']).reverse()
        a = fp.as_atom_obj()
        self.assertEqual(a.entries[0].title.text,
                         'Dream On Dreamer')
        self.assertEqual(a.entries[1].title.text,
                         'PID Namespaces in Linux')

    def test_map(self):
        def prepend_name(e):
            e.title = '[STATION] ' + e.title.text
            return e

        fp = FeedPipe().cat(['tests/eg.xml']).map(prepend_name)
        a = fp.as_atom_obj()
        self.assertEqual(
            a.entries[0].title.text,
            '[STATION] Migrating My Blog from Linode to CloudFront'
        )
        self.assertEqual(
            a.entries[1].title.text, '[STATION] UCSPI'
        )

    def test_grep(self):
        fp = FeedPipe() \
                .cat(['./tests/eg.xml']) \
                .grep(lambda e: 'e' in e.title.text)
        a = fp.as_atom_obj()
        self.assertEqual(
            a.entries[0].title.text,
            'Migrating My Blog from Linode to CloudFront'
        )
        self.assertEqual(
            a.entries[1].title.text,
            'Checking sudoers with visudo in SaltStack'
        )
        self.assertEqual(fp.count(), 5)

if __name__ == '__main__':
    unittest.main()
