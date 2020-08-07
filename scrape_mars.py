from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #executable_path = {"executable_path": "/Dataclass/chrome/chromedriver"}
    return Browser("chrome", headless=False)


def scrape_info():
    browser = init_browser()
    # Visit visit Mars News
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(10)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Get the results for all news
    results = soup.find_all('li', class_='slide')
    # Get the news title for first record
    news_title = results[0].find('div',class_='content_title').text
    # Get the news_p
    news_p = results[0].find('div',class_='article_teaser_body').text
    #scrape mars weather data
    url2 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url2)
    time.sleep(10)
    # Scrape page into Soup
    html2 = browser.html
    soup2 = bs(html2, "html.parser")
    temp = soup2.find_all(class_="css-1dbjc4n")[0]
    list_info = temp.find_all('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    for element in list_info:
        if element.text.find("InSight")!=-1:
            mars_weather = element.text
            break
    url3 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url3)
    time.sleep(10)
    # Scrape page into Soup
    html3 = browser.html
    soup3 = bs(html3, "html.parser")
    results = soup3.find('div', class_='carousel_items')
    print(type(results))
    image = results.article['style'].split("('")[1].split("'")[0]
    print(type(image))
    base_url = 'https://www.jpl.nasa.gov'
    featured_image_url  = base_url + image
    url4 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url4)
    df = tables[0]
    df.columns = [' ', 'Value']
    html_table = df.to_html(index= False)
    #scrape hem
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    time.sleep(10)
    # Scrape page into Soup
    html5 = browser.html
    soup5 = bs(html5, "html.parser")
    results = soup5.find_all('div', class_="item")
    links = []
    for x in results:
        link = x.find('a')['href']
        links.append(link)
    hemisphere_image_urls = []
    for link in links:
    #browser = Browser('chrome', headless=False)
        url2 = 'https://astrogeology.usgs.gov' + link
        browser.visit(url2)
        html = browser.html
        soup2 = bs(html, 'html.parser')
        title = soup2.find('h2', class_='title').text
        img_url =  soup2.find('li').a['href']
        new_dict = {"titles": title, "img_urls": img_url}
        hemisphere_image_urls.append(new_dict)
    
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title ,
        "news_p": news_p,
        "mars_weather": mars_weather,
        "featured_image_url":  featured_image_url,
        "html_table": html_table,
         "hemisphere_image_urls":hemisphere_image_urls        
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
