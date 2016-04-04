import sys
import re
import time
import os
from mechanize import Browser

filenm = str((sys.argv)[1])
url = "http://smog.rice.edu"

br = Browser()
br.set_handle_robots(False)
br.open(url+"/cgi-bin/GenTopGro.pl")

br.select_form(nr=0)

fp = open(filenm,"r")
br.form.add_file(fp, "text/plain", filenm, name='uploaded_file')

br["nickname"] = "mark"

br.submit()
fp.close()

time.sleep(5)

for link in br.links():
	loc = link.url.find("mark")
	if loc > 0:
		f = link.url[loc:]
		br.retrieve(url+link.url, os.path.join(os.getcwd(), f))
		break
