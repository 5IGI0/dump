import requests
import random
import json
import urllib3

with open("proxies.txt") as fp:
	proxies = fp.read().split("\n")

proxyActive = bool(proxies)

global poffset, session

poffset = 0
session = requests.session()

def switchProxy(pxy, reason):
	global poffset, session
	if pxy:
		proxies.remove(pxy["http"])
		print(f"proxy switching for \"{reason}\" ...")
		poffset = (1+poffset)%len(proxies)
		session = requests.session()

def get(url):
	global poffset, session
	tmp = None
	while tmp is None:
		pxy = {
				"http":proxies[poffset],
				"https":proxies[poffset]
			}
		try:
			tmp = session.get(url, proxies=pxy, timeout=(2.75, 3))
		except TimeoutError:
			switchProxy(pxy, "timeout")
			continue
		except requests.exceptions.ProxyError:
			switchProxy(pxy, "timeout")
			continue
		except requests.exceptions.ConnectTimeout:
			switchProxy(pxy, "timeout")
			continue
		except requests.exceptions.ConnectionError:
			switchProxy(pxy, "timeout")
			continue
		except requests.exceptions.ReadTimeout:
			switchProxy(pxy, "timeout")
			continue
		except requests.exceptions.ChunkedEncodingError:
			switchProxy(pxy, "chunk error")
			continue
		except urllib3.exceptions.ProtocolError:
			switchProxy(pxy, "Proto error")
			continue
		except ConnectionResetError:
			switchProxy(pxy, "conn reset")
			continue

		if "<title>Attention Required! | Cloudflare</title>" in tmp.text:
			switchProxy(pxy, "Cloudflare banned")
			tmp = None
		elif "Pastebin.com has blocked your IP" in tmp.text:
			switchProxy(pxy, "pastebin blocked")
			tmp = None
		elif "We've blocked you from the archive" in tmp.text:
			switchProxy(pxy, "pastebin blocked (archive page)")
			tmp = None
	return tmp
