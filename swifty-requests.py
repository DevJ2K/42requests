import requests
import json

url = "https://api.intra.42.fr/oauth/token"
body = {
	"grant_type": "client_credentials",
	"client_id": "",
	"client_secret": ""
}

try:
	response = requests.post(url, data=body)
	response.raise_for_status()
	token = response.json()
	print(token)
except Exception as e:
	print(f"Failed while fetching token: {e}")


def getLeaderboardURL() -> str:
	base  = "https://api.intra.42.fr/v2/cursus/21/cursus_users"
	base += "?filter[campus_id]=1" # Uniquement Paris
	# base += "?filter[user_id]=164784"
	base += "&sort=-level" # Trier dans l'ordre decroissant
	# base += "&detail=true"
	base += "&page[number]=1" # Numero de page
	base += "&page[size]=5" # Nombre d'utilisateurs par page
	base += "&range[begin_at]=2023-11-06T08:42:00.000Z,2023-11-06T08:42:00.000Z" # Promo de Novembre
	return base

def getURL(url: str, login: str) -> str:
	all_urls = {
		"users_list": f"https://api.intra.42.fr/v2/users?range%5Blogin%5D={login.lower()},{login.lower()}z",
		"find_by_campus": f"https://api.intra.42.fr/v2/campus/1/users?range%5Blogin%5D={login.lower()},{login.lower()}z&filter[staff?]=false",
		"user": f"https://api.intra.42.fr/v2/users/{login.lower()}",
		"users": f"https://api.intra.42.fr/v2/campus/1/users?filter[staff?]=false",
		"fetch": f"https://api.intra.42.fr/v2/campus/1/users?filter[active?]=true",
		"location": f"https://api.intra.42.fr/v2/campus/1/locations?range[host]=bess-f4,bess-f4z",
		"cursus": f"https://api.intra.42.fr/v2/cursus/21/cursus_users?filter[campus_id]=1&sort=-level&range[begin_at]=2023-09-03T07:42:00.000Z,2023-09-05T07:42:00.000Z",
		# "campus": f"https://api.intra.42.fr/v2/campus_users",
		"coalitions": f"https://api.intra.42.fr/v2/users/{login.lower()}/coalitions",
	}
	try:
		return all_urls[url]
	except:
		return ""

def getUserInfo(login: str):
	headers = {
		"Authorization": f"Bearer {token['access_token']}"
	}
	# print(headers)
	try:
		# response = requests.get(f"https://api.intra.42.fr/v2/users?range%5Blogin%5D={login.lower()},{login.lower()}z", headers=headers) # Fetching all users startswith
		url = getLeaderboardURL()
		# url = getURL("location", login)
		print(f"[{url}]")
		if (url == ""):
			print("Bad URL.")
			return
		response = requests.get(url, headers=headers) # Fetching all users startswith
		response.raise_for_status()
		with open("header.json", "w", encoding="utf-8") as f:
			# print(response.headers)
			f.write(json.dumps(dict(response.headers), indent=4))
		with open("output.json", "w", encoding="utf-8") as f:
			f.write(json.dumps(response.json(), indent=4))
		# print(json.dumps(response.json(), sort_keys=True, indent=4))
		# print(response.json())
	except Exception as e:
		print(f"Failed while fetching data: {e}")
	pass

getUserInfo("tajavon")
