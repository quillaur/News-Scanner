from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from tqdm import trange

def get_article_links(driver, url):
    driver.get(url)
    sleep(1)

    try:
        popup_consent = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Consent']")
        popup_consent.click()
        sleep(1)
    except NoSuchElementException:
        pass

    return driver.find_elements(By.CSS_SELECTOR, "a[rel='bookmark']")

url = "https://www.marktechpost.com/"

driver = webdriver.Chrome()

links = get_article_links(driver, url)

already_seen = []

for i in trange(len(links)):
    href = links[i].get_attribute("href")

    if href in already_seen:
        continue

    already_seen.append(href)

    links[i].click()
    sleep(0.5)
    
    article = driver.find_element(By.TAG_NAME, "article")

    title = article.find_element(By.TAG_NAME, "h1")
    with open(f"articles/{title.text}.txt", "w", encoding="utf-8") as txtf:
        txtf.write(article.text)
    
    links = get_article_links(driver, url)

driver.quit()