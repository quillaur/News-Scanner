import requests
from tqdm import trange

url = ('https://newsapi.org/v2/everything?'
       'q=AI&'
       'from=2023-08-30&'
       'language=en&'
       'sortBy=popularity&'
       'apiKey=74efa06ae8194772b5330249b1e7c011')

response = requests.get(url)

if response.status_code == 200:
    content = response.json()
    print(content["status"])
    print(content["totalResults"])

    for i in trange(5):
        article_id = f"article_{i}"
        with open(f"articles/{article_id}.txt", "w") as txtf:
            if content["articles"][i]["title"]:
                txtf.write(content["articles"][i]["title"])
                txtf.write(content["articles"][i]["description"])   
                txtf.write(content["articles"][i]["content"])

else:
    print("Error:", response.status_code)