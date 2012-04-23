# mi planeta particular con rawdog

Es una personalización de rawdog para crear un planeta bilingüe 
(español e inglés) con fuentes de noticias en sus correspondientes idiomas. Se 
actualizan al mismo tiempo.

Además he reescrito el modulo rss (original de Jonathan Riddell y adaptado por 
Adam Sampson y Roberto Alsina), para substituir la obsoleta (y con mayores 
dependencias) librería *`libxml2`* por la librería estándar *`xml.dom.minidom`*

### Carpetas en ./

* **en**:
 
 La configuración para el planet en inglés. Con fuentes de ejemplo en inglés.
  
* **es**:

 La configuración para el planet en español. Con fuentes de ejemplo en español.
 
* **planet**
 
 Donde se alojaran los planetas en esta configuración por defecto. Cada uno se 
 aloja en su carpeta correspondiente y comparten los elementos comunes a través 
 de enlaces simbólicos. 

* **plugins**
 
 Los plugins empleados para generar este planeta. 

### Archivos en ./
 
* **shell scripts**

 Son una serie de scripts que nos sirven para automatizar las tareas habituales 
 y para crear/borrar/explorar los planetas.
 
 * *browse.sh*
  
 Es script nos permite explorar los planetas con un navegador una vez creados. 
 Crea un servidor web temporal y abre el navegador en el planeta en español.
 
 * *clear.sh*
 
 Sirve para borrar los planetas y los ficheros state, para poder recrearlos 
 desde cero. Útil para tareas de depuración. Borrar para planetas en producción.
 
 * *create.sh*
 
 Este script en realidad lo que hace es llamar primero a `clear.sh` y luego a 
 `update.sh` para crear los planetas por primera vez o recrearlos desde cero.
 
 * *update.sh*
 
 Este script sería el único necesario en un planeta en producción. Lo que hace 
 es actualizar las fuentes de noticias y generar los ficheros html y xml 
 correspondientes. Es el script que ha de ejecutarse cada cierto tiempo para 
 hacer funcionar los planetas.

* **LEEME.markdown & README.markdown**

 Este fichero en versiones española e inglesa.
 
* **rawdog-2.12.tar.gz**

 rawdog package version 2.12
  
##  Instrucciones

 Requiere tener python instalado e instalar rawdog. Una vez instalado rawdog, 
 simplemente se corre el script `create.sh` para generar los planetas de 
 ejemplo. Si se realiza en local, se puede ejecutar `browse.sh` para visualizar
 inmediatamente el resultado. 

### IMPORTANTE

 Esta configuración solo trabaja bien con rawdog 2.12, en la versión 2.13 no se
 recogen las fechas de las fuentes
