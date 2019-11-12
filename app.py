import os
from bs4 import BeautifulSoup
import urllib.request
import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

base_url = 'http://202.58.181.161:88/prototype_santoleo/#id=gewc5z&p=login&g=1'

# init driver
profile = webdriver.FirefoxProfile()
profile.set_preference("javascript.enabled", True)
driver = webdriver.Firefox(profile)
driver.get(base_url)

WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "sitemapHeader")))
soup = BeautifulSoup(driver.page_source, "html")

soap_sitemap_tree_container = soup.find("div", {"id": "sitemapTreeContainer"})

def get_menu_items(soup):
    menus = []
    soap_sitemap_tree = soup.find("ul")
    if soap_sitemap_tree == None: 
        return menus

    soap_menus = soap_sitemap_tree.find_all("li", {"class": "sitemapNode"}, recursive=False)
    
    for soap_menu in soap_menus:
        soap_menu_title = soap_menu.find("span", {"class": "sitemapPageName"})
        menus.append({ "curr": soap_menu_title.text, "children": get_menu_items(soap_menu) })
    return menus

menus = get_menu_items(soap_sitemap_tree_container)

