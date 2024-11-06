import bs4

def getUserInfos(pageCode):
	data = {"name": "guest", "url":"https://pastebin.com", "icon_url":"https://pastebin.com/i/facebook.png"}
	soup = bs4.BeautifulSoup(pageCode, "html.parser")
	
	try:
		data["name"] = soup.find("div", {"class":"paste_box_line2"}).find("a").getText()
		data["url"] = "https://pastebin.com/u/"+data["name"]

		tmp = "https:"+soup.find("img", {"class":"i_gb"})["src"]
		
		if tmp == "https:/i/t.gif":
			return data

		data["icon_url"] = tmp
	except:
		pass
	
	return data