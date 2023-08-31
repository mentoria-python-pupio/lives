import requests

url = "https://chaos-data.projectdiscovery.io/index.json"

payload={}
# headers = {
#   'authority': 'www.fundsexplorer.com.br',
#   'accept': 'application/json, text/plain, */*',
#   'referer': 'https://www.fundsexplorer.com.br/ranking',
#   'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
#   'sec-ch-ua-platform': '"Linux"',
#   'sec-fetch-site': 'same-origin',
#   'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
#   'x-funds-nonce': '61495f60b533cc40ad822e054998a3190ea9bca0d94791a1da'
# }

response = requests.request("GET", url, data=payload)

print(response.text)

