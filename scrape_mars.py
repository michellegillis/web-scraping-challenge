from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import os
import re
import requests
import pymongo
import pandas as pd
import re

def init_browser():
    executable_path = {"executable_path": r"C:/Users/Michelle/Desktop/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def info_scrape(browser):
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    try:
        news_title = soup.find('div', class_="content_title").text
        news_p = soup.find('div', class_="rollover_description_inner").text
    except:
        return(None)

    return(news_title, news_p)

def image_scrape(browser):
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    image = browser.find_by_id('full_image')
    image.click()
    more_info = browser.links.find_by_partial_text('more info')
    more_info.click()
    link = browser.html
    img_soup = bs(link, 'html.parser')
    try:
        full_image = img_soup.select_one('figure.lede a img')
        full_url = full_image.get("src")    
    except:
        return(None)
    featured_image_url = 'https://jpl.nasa.gov' + full_url
    return(featured_image_url)

def twit_scrape(browser):
    twit_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twit_url)
    twit = browser.html
    twit_soup = bs(twit, 'html.parser')
    try:
        tweets=twit_soup.find_all("span",text=re.compile('InSight sol'))
    except:
        return(None)
    mars_weather = tweets[0].get_text()
    return(mars_weather)

def table_scrape(browser):
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    tables = pd.read_html(facts_url)
    mars_facts = tables[0]
    mars_facts_html = mars_facts.to_html()
    mars_facts_html.replace('\n','')
    return(mars_facts.to_html('marsfacts.html'))

def scrape_all():
    browser = Browser("")
    title = info_scrape(browser)
    paragraph_body = info_scrape(browser)
    img = image_scrape(browser)
    weather = twit_scrape(browser)
    table = table_scrape(browser)
    data = {
        "News Title": title,
        "Paragraph": paragraph_body,
        "Image" : img,
        "Recent Weather" : weather,
        "Fun Facts" : table
    }    
    return (data)












 
