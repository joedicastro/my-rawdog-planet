"""
paged-output plugin for rawdog, by Adam Sampson <ats@offog.org>

Needs rawdog 2.5rc1 or later.

Rather than writing a single output file, split the output into several files
with "articlesperpage" entries in each one. Generate a __paged_output_pages__
bit in the main template that lists the files and the date of the latest entry
in each.
"""

import os
import rawdoglib.plugins
from rawdoglib.rawdog import DayWriter, write_ascii, format_time, fill_template
from StringIO import StringIO

articles_per_page = 100

def config_option(config, name, value):
	if name == "articlesperpage":
		global articles_per_page
		articles_per_page = int(value)
		return False
	else:
		return True

def output_write_files(rawdog, config, articles, article_dates):
	config.log("paged-output starting")

	outputfile = config["outputfile"]
	i = outputfile.rfind('.')
	if i != -1:
		prefix = outputfile[:i]
		suffix = outputfile[i:]
	else:
		prefix = outputfile
		suffix = ""

	chunks = []
	while articles != []:
		chunks.append(articles[:articles_per_page])
		articles = articles[articles_per_page:]

	fns = []
	for i in range(len(chunks)):
		if i == 0:
			fn = prefix + suffix
		else:
			fn = "%s%d%s" % (prefix, i, suffix)
		fns.append(fn)

	for i in range(len(chunks)):
		fn = fns[i]
		date = format_time(article_dates[chunks[i][0]], config)
		config.log("paged-output writing ", fn, " (", date, ")")

		f = StringIO()
		dw = DayWriter(f, config)
		for article in chunks[i]:
			dw.time(article_dates[article])
			rawdog.write_article(f, article, config)
		dw.close()

		bits = rawdog.get_main_template_bits(config)
		bits["items"] = f.getvalue()
		bits["num_items"] = str(len(rawdog.articles.values()))

		f = StringIO()
		f.write('<ul class="paged_output_pages">\n')
		for j in range(len(chunks)):
			first = chunks[j][0]
			f.write('<li>')
			if i != j:
				f.write('<a href="' + os.path.basename(fns[j]) + '">')
			f.write(format_time(article_dates[first], config))
			if i != j:
				f.write('</a>')
			f.write('</li>\n')
		f.write('</ul>\n')
		bits["paged_output_pages"] = f.getvalue()

		s = fill_template(rawdog.get_template(config), bits)
		f = open(fn + ".new", "w")
		write_ascii(f, s, config)
		f.close()
		os.rename(fn + ".new", fn)

	config.log("paged-output done")
	return False

rawdoglib.plugins.attach_hook("config_option", config_option)
rawdoglib.plugins.attach_hook("output_write_files", output_write_files)
