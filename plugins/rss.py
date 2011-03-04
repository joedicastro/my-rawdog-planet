# -*- coding: utf-8 -*-
#
# rawdog plugin to generate RSS, OPML and FOAF output
# Copyright 2008 Jonathan Riddell
# Copyright 2009 Adam Sampson <ats@offog.org>
# Copyright 2009 Roberto Alsina
# Copyright 2011 joe di castro <joe@joedicastro.com>
#
# rawdog_rss is free software; you can redistribute and/or modify it
# under the terms of that license as published by the Free Software
# Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# rawdog_rss is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rawdog_rss; see the file COPYING. If not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA, or see http://www.gnu.org/.
#
# ---
#
# This plugin supports the following configuration options:
#
# outputxml         RSS output filename
# outputfoaf        FOAF output filename
# outputopml        OPML output filename
# xmltitle          Feed title (e.g. "Planet Foo")
# xmllink           Feed link (e.g. "http://planet-foo.example.com/")
# xmllanguage       Feed language (e.g. "en")
# xmlurl            URL of the generated RSS (e.g. "http://planet-foo.example.com/rss20.xml")
# xmldescription    Feed description (e.g. "People who work on foo")
# xmlownername      Feed owner's name
# xmlowneremail     Feed owner's email address
# xmlmaxarticles    Maximum number of articles to include in the feed
#                   (defaults to maxarticles if not specified)
#
# If you're using rawdog to produce a planet page, you'll probably want to have
# "sortbyfeeddate true" in your config file too.

import os, time, cgi
import rawdoglib.plugins, rawdoglib.rawdog

from rawdoglib.rawdog import detail_to_html, string_to_html
from time import gmtime, strftime
from xml.dom.minidom import Document

def rfc822_date(tm):
    """Format a GMT timestamp as returned by time.gmtime() in RFC822 format.
    (This is insensitive to the current locale.)"""
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
        ]
    return "%s, %02d %s %04d %02d:%02d:%02d GMT" % \
        (days[tm[6]], tm[2], months[tm[1] - 1], tm[0], tm[3], tm[4], tm[5])

class RSS_Feed:
    def __init__(self):
        self.options = {
            "outputxml": "rss20.xml",
            "outputfoaf": "foafroll.xml",
            "outputopml": "opml.xml",
            "xmltitle": "Planet KDE",
            "xmllink": "http://planetKDE.org/",
            "xmllanguage": "en",
            "xmlurl": "http://planetKDE.org/rss20.xml",
            "xmldescription": "Planet KDE - http://planetKDE.org/",
            "xmlownername": "Jonathan Riddell",
            "xmlowneremail": "",
            "xmlmaxarticles": ""
            }

    def config_option(self, config, name, value):
        if name in self.options:
            self.options[name] = value
            return False
        else:
            return True

    def feed_name(self, feed, config):
        """Return the label used for a feed. If it has a "name" define, use
        that; otherwise, use the feed title."""

        if "define_name" in feed.args:
            return feed.args["define_name"]
        else:
            return feed.get_html_name(config)

    def article_to_xml(self, xml_article, xml_doc, rawdog, config, article):
        entry_info = article.entry_info

        id = entry_info.get("id", self.options["xmlurl"] + "#id" + article.hash)

        guid = xml_doc.createElement('guid')
        guid_txt = xml_doc.createTextNode(string_to_html(id, config))
        guid.setAttribute('isPermaLink', 'false')
        guid.appendChild(guid_txt)
        xml_article.appendChild(guid)

        title = self.feed_name(rawdog.feeds[article.feed], config)
        s = detail_to_html(entry_info.get("title_detail"), True, config)
        title = title.decode('utf-8')
        if s is not None:
            title += u": " + s
        title = title.encode('utf-8')

        xml_article_title = xml_doc.createElement('title')
        xml_article_title_txt = xml_doc.createTextNode(title)
        xml_article_title.appendChild(xml_article_title_txt)
        xml_article.appendChild(xml_article_title)

        if article.date is not None:
            date = rfc822_date(gmtime(article.date))

            xml_article_date = xml_doc.createElement('pubDate')
            xml_article_date_txt = xml_doc.createTextNode(date)
            xml_article_date.appendChild(xml_article_date_txt)
            xml_article.appendChild(xml_article_date)

        s = entry_info.get("link")
        if s is not None and s != "":
            xml_article_link = xml_doc.createElement('link')
            xml_article_link_txt = xml_doc.createTextNode(string_to_html(s, config))
            xml_article_link.appendChild(xml_article_link_txt)
            xml_article.appendChild(xml_article_link)

        for key in ["content", "summary_detail"]:
            s = detail_to_html(entry_info.get(key), False, config)
            if s is not None:
                xml_article_description = xml_doc.createElement('description')
                xml_article_description_txt = xml_doc.createTextNode(s)
                xml_article_description.appendChild(xml_article_description_txt)
                xml_article.appendChild(xml_article_description)
                break

        return True

    def write_rss(self, rawdog, config, articles):
        doc = Document()

        rss = doc.createElement('rss')
        rss.setAttribute('version', "2.0")
        rss.setAttribute('xmlns:dc', "http://purl.org/dc/elements/1.1/")
        rss.setAttribute('xmlns:atom', 'http://www.w3.org/2005/Atom')
        doc.appendChild(rss)

        channel = doc.createElement('channel')
        rss.appendChild(channel)

        title = doc.createElement('title')
        title_txt = doc.createTextNode(self.options["xmltitle"])
        title.appendChild(title_txt)
        channel.appendChild(title)

        link = doc.createElement('link')
        link_txt = doc.createTextNode(self.options["xmllink"])
        link.appendChild(link_txt)
        channel.appendChild(link)

        language = doc.createElement('language')
        language_txt = doc.createTextNode(self.options["xmllanguage"])
        language.appendChild(language_txt)
        channel.appendChild(language)

        description = doc.createElement('description')
        description_txt = doc.createTextNode(self.options["xmldescription"])
        description.appendChild(description_txt)
        channel.appendChild(description)

        atom_link = doc.createElement('atom:link')
        atom_link.setAttribute('href', self.options["xmlurl"])
        atom_link.setAttribute('rel', 'self')
        atom_link.setAttribute('type', 'application/rss+xml')
        channel.appendChild(atom_link)

        try:
            maxarticles = int(self.options["xmlmaxarticles"])
        except ValueError:
            maxarticles = len(articles)
        for article in articles[:maxarticles]:
             xml_article = doc.createElement('item')
             channel.appendChild(xml_article)
             self.article_to_xml(xml_article, doc, rawdog, config, article)

        with open(self.options["outputxml"], 'w') as rss:
            rss.write(doc.toprettyxml(indent="    "))

    def write_foaf(self, rawdog, config):
        doc = Document()

        xml = doc.createElement('rdf:RDF')

        xml.setAttribute('xmlns:rdf', "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        xml.setAttribute('xmlns:rdfs', "http://www.w3.org/2000/01/rdf-schema#")
        xml.setAttribute('xmlns:foaf', "http://xmlns.com/foaf/0.1/")
        xml.setAttribute('xmlns:rss', "http://purl.org/rss/1.0/")
        xml.setAttribute('xmlns:dc', "http://purl.org/dc/elements/1.1/")
        doc.appendChild(xml)

        group = doc.createElement('foaf:Group')
        xml.appendChild(group)

        foaf_name = doc.createElement('foaf:name')
        foaf_name_txt = doc.createTextNode(self.options["xmltitle"])
        foaf_name.appendChild(foaf_name_txt)
        group.appendChild(foaf_name)

        foaf_homepage = doc.createElement('foaf:homepage')
        foaf_homepage_txt = doc.createTextNode(self.options["xmllink"])
        foaf_homepage.appendChild(foaf_homepage_txt)
        group.appendChild(foaf_homepage)

        seeAlso = doc.createElement('rdfs:seeAlso')
        seeAlso.setAttribute('rdf:resource', '')
        group.appendChild(seeAlso)

        for url in sorted(rawdog.feeds.keys()):
            member = doc.createElement('foaf:member')
            group.appendChild(member)

            agent = doc.createElement('foaf:Agent')
            member.appendChild(agent)

            agent_foaf_name = doc.createElement('foaf:name')
            agent_foaf_name_txt = doc.createTextNode(self.feed_name(rawdog.feeds[url], config))
            agent_foaf_name.appendChild(agent_foaf_name_txt)
            agent.appendChild(agent_foaf_name)

            weblog = doc.createElement('foaf:weblog')
            agent.appendChild(weblog)

            document = doc.createElement('foaf:Document')
            document.setAttribute('rdf:about', url)
            weblog.appendChild(document)

            seealso = doc.createElement('rdfs:seeAlso')
            document.appendChild(seealso)

            channel = doc.createElement('rss:channel')
            channel.setAttribute('rdf:about', '')
            seealso.appendChild(channel)

        with open(self.options["outputfoaf"], 'w') as foaf:
            foaf.write(doc.toprettyxml(indent="   "))

    def write_opml(self, rawdog, config):
        doc = Document()

        xml = doc.createElement('opml')
        xml.setAttribute('version', "1.1")
        xml.setAttribute('encoding', "utf-8")
        doc.appendChild(xml)

        head = doc.createElement('head')
        xml.appendChild(head)

        title = doc.createElement('title')
        title_txt = doc.createTextNode(self.options["xmltitle"])
        title.appendChild(title_txt)
        head.appendChild(title)
        now = rfc822_date(gmtime())
        created = doc.createElement('dateCreated')
        created_text = doc.createTextNode(now)
        created.appendChild(created_text)
        head.appendChild(created)
        modified = doc.createElement('dateModified')
        modified_txt = doc.createTextNode(now)
        modified.appendChild(modified_txt)
        head.appendChild(modified)
        own_name = doc.createElement('ownerName')
        own_name_txt = doc.createTextNode(self.options["xmlownername"])
        own_name.appendChild(own_name_txt)
        head.appendChild(own_name)
        own_email = doc.createElement('ownerEmail')
        own_email_txt = doc.createTextNode(self.options["xmlowneremail"])
        own_email.appendChild(own_email_txt)
        head.appendChild(own_email)

        body = doc.createElement('body')
        xml.appendChild(body)

        for url in sorted(rawdog.feeds.keys()):
            outline = doc.createElement('outline')
            outline.setAttribute('text', self.feed_name(rawdog.feeds[url], config))
            outline.setAttribute('type', 'rss')
            outline.setAttribute('xmlUrl', url)
            outline.setAttribute('htmlUrl', rawdog.feeds[url].feed_info.get("link"))
            outline.setAttribute('title', rawdog.feeds[url].get_html_name(config))
            body.appendChild(outline)

        with open(self.options["outputopml"], 'w') as opml:
            opml.write(doc.toprettyxml(indent="   "))

    def output_write(self, rawdog, config, articles):
        self.write_rss(rawdog, config, articles)
        self.write_foaf(rawdog, config)
        self.write_opml(rawdog, config)

        return True

rss_feed = RSS_Feed()
rawdoglib.plugins.attach_hook("config_option", rss_feed.config_option)
rawdoglib.plugins.attach_hook("output_write", rss_feed.output_write)
