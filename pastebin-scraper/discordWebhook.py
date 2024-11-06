import requests
import json
import tools

with open("config.json") as fp:
	config = json.load(fp)

def on_match(code, match, r, regexmatch, paste):

	payload = {
		"embeds": [{
			"title":"new match !",
			"url":"https://pastebin.com/"+code,
			"author": tools.getUserInfos(r.text),
			"fields" : [
				{
					"name": "paste",
					"value": code,
					"inline":False
				},
				{
					"name": "match's name",
					"value": match["name"],
					"inline":True
				}
			]
		}]
	}
	if not regexmatch is None:
		payload["embeds"][0]["fields"].append({
			"name": "match",
			"value": regexmatch
		})
	alt_url = requests.post("http://bin.shaa.ga/create.php",data={
		"text":paste
	}).url
	payload["embeds"][0]["fields"].append({
		"name": "download links",
		"value": f"[pastebin](https://pastebin.com/{code})\n[bin.shaa.ga]({alt_url})"
	})
	for collection in match["collections"]:
		if collection in config["discordWebhooks"].keys():
			print(requests.post(config["discordWebhooks"][collection], data=json.dumps(payload), headers={"Content-Type":"application/json"}).text)