import requester
import bs4
import time
import _paste

i = 1

while True:
	r = requester.get("https://pastebin.com/archive")
	soup = bs4.BeautifulSoup(r.text, "html.parser")
	tmp = soup.find("table", attrs={"class":"maintable"})
	if tmp is None:
		i += 1
		# with open("tmp.html", "w") as fp:
		# 	fp.write(r.text)
		print("menu not found !")
		time.sleep(5)
		if i %5:
			i=1
			requester.switchProxy({"http":requester.proxies[requester.poffset]}, "menu not found !")
		continue
	
	for link in tmp.find_all('a'):
		if "archive" in link.get('href'):
			continue
		_paste.on_paste(link.get('href')[1:])
	
	time.sleep(1.25)
