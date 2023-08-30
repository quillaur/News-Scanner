from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

url = "https://www.marktechpost.com/"
driver = webdriver.Chrome()

driver.get(url)
sleep(30)

driver.quit()

# if response.status_code == 200:
#     print("Success !")

#     soup = BeautifulSoup(response.text, "html.parser")

#     links = soup.find_all("a", rel="bookmark")
#     hrefs = list(set([l.get("href") for l in links if l]))
    
#     for href in hrefs:
#         print(href)
#         sleep(0.1)
#         response = requests.get(url)

#         if response.status_code == 200:
#             print("Success !")

#             soup = BeautifulSoup(response.text, "html.parser")

#             article = soup.find("article")
#             print(article)
#             name = href.split("/")[-1]
#             with open(f"{name}.txt", "w") as txtf:
#                 txtf.write(article.text)
#         else:
#             print("Echec, error code:", response.status_code)

# else:
#     print("Echec, error code:", response.status_code)