import requester
import os
import json
import re
import bs4

with open("config.json") as fp:
	config = json.load(fp)

def on_paste(code):
	if not os.path.isfile(f"datas/{code}"):
		print(f"new paste : {code}")
		r = requester.get(f"https://pastebin.com/{code}")
		soup = bs4.BeautifulSoup(r.text, "html.parser")
		try:
			paste = soup.find("textarea", {"id":"paste_code"}).getText()
		except:
			return
		with open(f"datas/{code}", "w") as fp:
			fp.write(paste)
		# return
		
		if len(paste) > 50000:
			return
		for match in config["matches"]:
			if match["type"] == "text":
				pass
			elif match["type"] == "regex":
				m = [x.group() for x in re.finditer(match["regex"], paste)]
				if len(m):
					with open(f"match-{match['name']}.txt", "a") as fp:
						for mt in m:
							fp.write(mt+"\n")

if __name__ == "__main__":
	on_paste("gGy6xTw2")

