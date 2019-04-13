def scrape():

    from splinter import Browser
    from splinter.exceptions import ElementDoesNotExist
    from bs4 import BeautifulSoup as bs
    import requests
    import pandas as pd
    
    # bs4 is not pulling the correct content. I'm using splinter to get the data
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit('https://mars.nasa.gov/news')

    html = browser.html

    soup = bs(html, 'html.parser')

    #Use BS to find all the content titles, then save the first one as a variable
    results = soup.find_all('div', class_='content_title')
    news_title = results[0].text.strip()

    #The description of the article is held in a class called 'rollover_description_inner'. Pull the first one and store it.
    results = soup.body.find_all('div', class_='rollover_description_inner')
    news_p = results[0].text.strip()

    #Direct the browser to the JPL space images site
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    #Extract the html and pass it into BS
    soup = bs(browser.html, 'html.parser')

    #The featured image button (button fancybox) has the relative address of the featured image in the a tag
    results = soup.find('a', class_='button fancybox')
    tail = results['data-fancybox-href']

    #We append the relative address to the main URL to get the full link
    featured_image_url = 'https://www.jpl.nasa.gov' + tail   

    # Use the response libary read the URL and output the text to Beautiful Soup
    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    # Find all the tweets on the first page and extract the text from the first one
    tweets = soup.find_all('div', class_='js-tweet-text-container')
    mars_weather = tweets[0].text.strip()

    #Pull the html for the space facts site
    url = 'https://space-facts.com/mars/'
    response = requests.get(url)

    #Pull the table into pandas
    facts = pd.read_html(response.text, attrs = {'id':"tablepress-mars"})
    facts_df = facts[0]

    #Pull the table out of padas
    facts_table = facts_df.to_html(header=False, index=False)

    #Call a browser with splinter
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')

    #Pull the html from the browser and pull the hrefs from the links
    soup = bs(browser.html, 'html.parser')
    hemispheres = soup.find_all('div', class_="description")

    #Loop though the urls and pull the image urls
    hemisphere_image_urls = []
    for item in hemispheres:
        title = item.h3.text
        url_tail = item.a['href']
        url = 'https://astrogeology.usgs.gov' + url_tail
        browser.visit(url)
        img_url = browser.find_by_text('Sample')['href']
        hemisphere_image_urls.append({title:img_url})

    browser.quit()

    return {'news_title':news_title, 'news_p':news_p, 'featured_image_url':featured_image_url,
    'mars_weather':mars_weather, 'facts_table':facts_table, 'hemisphere_image_urls':hemisphere_image_urls
    }