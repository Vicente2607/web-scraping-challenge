from splinter import Browser
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)



# Defining scrape & dictionary

def scrape():

    final_data = {}
    output = marsNews()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_weather"] = mars_weather()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()



    return final_data



# # NASA Mars News



def marsNews():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    articulo = soup.find("div", class_='list_text')
    titulo = articulo.find("div", class_="content_title").text
    contenido = articulo.find("div", class_ ="article_teaser_body").text
    output = [titulo, contenido]
    browser.quit()

    return output



# # JPL Mars Space Images - Featured Image

def marsImage():
    browser = init_browser()
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    browser.quit()

    return featured_image_url



# # Mars Weather

def mars_weather():
    browser = init_browser()
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    weather = soup.find_all(class_ = "css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    weather = weather[27].text
    weather = weather.replace('\n', ' ')
    weather = weather.replace('InSight ', '')
    mars_weather = {
        'weather': weather
        }

    browser.quit()

    return mars_weather




# # Mars Facts

def marsFacts():
    browser = init_browser()
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(header = False, index = False)
    browser.quit()

    return mars_facts





# # Mars Hemispheres

def marsHem():
    browser = init_browser()
    url2 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url2)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    products = soup.find("div", class_ = "result-list" )
    hemisferios = products.find_all("div", class_="item")
    hemisferios_marte = []
    for hemisferio in hemisferios:
        titulo = hemisferio.find("h3").text
        titulo = titulo.replace("Enhanced", "")
        final = hemisferio.find("a")["href"]
        imagen_link = "https://astrogeology.usgs.gov/" + final    
        browser.visit(imagen_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisferios_marte.append({"title": titulo, "img_url": image_url})
    browser.quit()

    return hemisferios_marte