#! /usr/bin/env python
from selenium import webdriver
from bs4 import BeautifulSoup

# Inputs: 
# Dates should be in format YYYY-MM-DD.
def scrape(query, startDate, endDate):

	#Initiate webdriver
	url='https://twitter.com/search?q=' + query + ' since%3A' + startDate + ' until%3A' +endDate
	driver = webdriver.Firefox()
	driver.get(url)

	# Use webdriver to load entire page through end of results
	# Loop identifies bottom of page by seeing the same time stamp 10 times in a row. 
	sametimeNum = 0
	lastTime = ""
	while (sametimeNum<10):	
		timestamps=driver.find_elements_by_xpath("//li[@data-item-type='tweet']//div[@class='content']//small[@class='time']/a")
		if timestamps[-1].get_attribute('title') == lastTime:
			sametimeNum = sametimeNum+1
		else:
			sametimeNum = 0
		lastTime = timestamps[-1].get_attribute('title')
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	# Load page into beautifulsoup and scrape
	soup = BeautifulSoup(driver.page_source)

	usernames = soup.find_all(class_='username js-action-profile-name')
	timestamps = soup.find_all(class_='tweet-timestamp js-permalink js-nav js-tooltip')
	tweets = soup.find_all(class_='TweetTextSize  js-tweet-text tweet-text')

	# Write to output list
	tweetsOut=[]
	for i in range(0,len(usernames)):
		username=usernames[i].text
		timestamp=timestamps[i].get('title')
		tweet=str(tweets[i].text.encode("utf-8"))
		tweetsOut.append([i, username, timestamp, tweet])

	driver.quit()

	return(tweetsOut)

