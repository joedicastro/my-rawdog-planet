<!-- -*- markdown -*- -->

# my rawdog personal planet

It is a customized rawdog to create a bilingual planet (Spanish & English) with 
news feeds in their respective languages. Both are updated at the same time.

I've also rewritten the rss module (originally by Jonathan Riddell and adapted 
by Adam Sampson and Roberto Alsina), to replace the deprecated (and with 
greater dependencies) *`libxml2`* library by the standard library 
*`xml.dom.minidom`*

### Folders in ./

* **en**:

 The settings for the planet in English. Sample news feeds in English.
  
* **es**:

 The settings for the planet in Spanish. Sample news feeds in Spanish.

* **planet**
 
 The place where the planets were generated in this settings by default. Each 
 is stored in its corresponding folder and share common elements through 
 symbolic links.
 
* **plugins**
 
 The plugins used to generate this planet.
 
### Files in ./

* **shell scripts**

 Are a series of scripts that we use to automate common tasks and 
 create/delete/explore the planets.
 
 * *browse.sh*
 
 This script allows us to explore the planets with a web browser once created. 
 Creates a temporary web server and opens the browser on the planet in Spanish.
  
 * *clear.sh*
 
 Allows you to delete the planets and the state files to be able to recreate 
 them from scratch. Useful for debugging. Delete this for planets in production.
 
 * *create.sh*
 
 This script actually does is to call first to `clear.sh` and then `update.sh` 
 to create the planets for the first time or recreate them from scratch.
 
 * *update.sh*
 
 This script would be the only necessary in a planet in production. What it does
 is update news sources and generate html and xml files accordingly. It is the 
 script to be executed periodically to run the planet.
 
* **README.markdown & LEEME.markdown**

 This file in English and Spanish versions. 
 
## Instructions

 You need to have python installed and install rawdog. Once installed rawdog, 
 simply run the script `create.sh` to generate the sample planets. If done 
 locally, you can run `browse.sh` to display the results immediately.
   
### IMPORTANT

 It's works well only with rawdog 2.12, in 2.13 version don't get the feeds date