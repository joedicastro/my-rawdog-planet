<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">
<html lang="es">
<%def name="title()">
    mi planeta personal
</%def>

<%def name="xmls()">
    <a href="http://localhost:8000/planet/es/foafroll.xml"><img src="foaf.png" title="FOAF"></a>
    <a href="http://localhost:8000/planet/es/opml.xml"><img src="opml.png" title="OPML"></a>
    <a href="http://localhost:8000/planet/es/rss.xml"><img src="rss.png" title="RSS"></a>
</%def>
<%def name="lang()">
    <a href="http://localhost:8000/planet/es/"><img src="es_ES.png" title="ES"></a>
    <a href="http://localhost:8000/planet/en/"><img src="en_GB.png" title="EN"></a>
</%def>
<%def name="log()">
    <a href="http://localhost:8000/planet/es/log.html">Estado de fuentes</a>
</%def>
<%def name="validrss()">
</%def>
<%def name="opmlfile()">
    <% return '../planet/es/opml.xml' %>
</%def>
<%def name="readopml(opml)">
<%
    from xml.dom.minidom import parse, parseString
    import urllib2

    dom1 = parseString(open(opml).read())
    links = dom1.getElementsByTagName('outline')
    feedlist=''
    links_dict = []
    for link in links:
        links_dict.append({'text':link.getAttribute('text'),
                            'htmlUrl':link.getAttribute('htmlUrl'),
                             'xmlUrl':link.getAttribute('xmlUrl')})

    for link in sorted(links_dict, key=lambda links_dict : links_dict['text'].lower()):
        linktext = '<a href="%s">%s</a>\n'%(link['htmlUrl'],
                                            link['text'])
        flinktext= '<a href="%s"><img src="feed-icon.png"></a>\n'%link['xmlUrl']

        feedlist+=linktext
        feedlist+=flinktext
        feedlist+='<br>\n'
    return feedlist
%>
</%def>

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="robots" content="noarchive">
    ${refresh}.
    <link rel="shortcut icon" href="favicon.ico" type="image/vnd.microsoft.icon" />
    <link rel="stylesheet" href="style.css" type="text/css">
    <link rel="alternate" type="application/rss+xml" title="${self.title()}" href="http://localhost:800/planet/es/rss.xml"" />
    <title>${self.title()}</title>
</head>
<body id="rawdog">
<div id="header">
<h1><img src="banner_es.png" alt="${self.title()}"></h1>
</div>
<div id="items">
${items}
</div>
<div id="feedstats">
    <div id="xmls">
        ${self.xmls()}
    </div>
    <h2 id="feedstatsheader">Idioma</h2>
    <div id="log">
        ${self.lang()}
    </div>
    <h2 id="feedstatsheader">Estado</h2>
    <div id="log">
        ${self.log()}
    </div>
    <h2 id="feedstatsheader">Archivo</h2>
    <div id="archive"">
        ${dated_output_calendar}
    </div>
    <h2 id="feedstatsheader">Blogs</h2>
    <div id="feedlist">
        ${self.readopml(self.opmlfile())}
    </div>
</div>
<div id="footer">
<p id="aboutrawdog">Generado por
<a href="http://offog.org/code/rawdog.html">rawdog</a>
version ${version}
by <a href="mailto:ats@offog.org">Adam Sampson</a>.</p>
<p>Basado en el <a href="http://github.com/ralsina/planeta-pyar/tree/master">trabajo de Roberto Alsina</a> para PyAr</p>
<p>
${self.validrss()}
</p>
</div>
</body>
</html>

