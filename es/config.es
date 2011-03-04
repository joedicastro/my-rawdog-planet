# Donde se generara el planeta
outputfile ../planet/es/index.html

# La plantilla a emplear
template template.es

# La plantilla para cada entrada
itemtemplate itemtemplate

# Generacion de los archivos RSS, OPML y FOAF
outputxml ../planet/es/rss.xml
outputfoaf ../planet/es/foafroll.xml
outputopml ../planet/es/opml.xml
xmlmaxarticles 30
xmltitle mi planeta particular
xmllink http://localhost:8000/es
xmllanguage es
xmldescription mis fuentes de noticias
xmlownername joe di castro
xmlowneremail joe@joedicastro.com

# Salida del registro de estado de las fuentes
statuslogfile ../planet/es/log
statusoutputfile ../planet/es/log.html

# Articulos por pagina del archivo
articlesperpage 30

# Fuentes de noticias del planeta

feed 30m http://feeds.feedburner.com/PlanetUbuntuEs
    define_name Planet Ubuntu ES
    
feed 30m http://www.hispalinux.es/node/feed
	define_name Hispalinux
	
feed 30m http://backends.barrapunto.com/barrapunto.rss
	define_name Barrapunto
	
feed 30m http://feeds2.feedburner.com/diegocg
	define_name D'Oh!
	
feed 30m http://www.sahw.com/wp/feed/
	define_name Sergio Hernando
	
feed 30m http://python.majibu.org/feeds/rss
	define_name python majibu


