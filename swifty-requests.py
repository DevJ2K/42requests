import requests
import json

url = "https://api.intra.42.fr/oauth/token"
body = {
	"grant_type": "client_credentials",
	"client_id": "u-s4t2ud-38f265289b75e04059b7a400daa7b92dcecaf7b762214f0d9f1456d9174bf8fe",
	"client_secret": "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"
}

try:
	response = requests.post(url, data=body)
	response.raise_for_status()
	token = response.json()
	print(token)
except Exception as e:
	print(f"Failed while fetching token: {e}")



def getUserInfo(login: str):
	headers = {
		"Authorization": f"Bearer {token['access_token']}"
	}
	print(headers)
	try:
		# response = requests.get(f"https://api.intra.42.fr/v2/users?range%5Blogin%5D={login.lower()},{login.lower()}z", headers=headers) # Fetching all users startswith
		response = requests.get(f"https://api.intra.42.fr/v2/users/{login.lower()}/coalitions", headers=headers) # Fetching all users startswith
		response.raise_for_status()
		with open("output.json", "w") as f:
			f.write(json.dumps(response.json(), sort_keys=True, indent=4))
		# print(json.dumps(response.json(), sort_keys=True, indent=4))
		# print(response.json())
	except Exception as e:
		print(f"Failed while fetching data: {e}")
	pass

getUserInfo("tajavon")
