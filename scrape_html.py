import codecs
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import random, time, requests
import threading
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import codecs
import csv
def update_csv(data_array):
    with codecs.open(r'result.csv', 'a',encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(data_array)

update_csv(['Corporation Name','Name','Location','Rating Score','Rating Date','Review Title','Review Content'])
def get_review_content(review_url):
    review_page=requests.get(review_url)
    soup_review = BeautifulSoup(review_page.content, "html.parser")
    main_review_div = soup_review.find("div", {"class": "review hsx_review is-multiline is-mobile inlineReviewUpdate provider0"})
    main_name_div =soup_review.find("div", {"class": "surContent"})
    main_score_h1 = soup_review.find("h1", {"id": "HEADING"})
    result_data=[]
    try:
        co_name = main_name_div.find('a').text
        result_data.append(co_name)
        # print("Corporation",co_name)
    except:
        result_data.append('')
        # print("Corporation",'')

    try:
        review_name=main_review_div.find("div", {"class": "username mo"}).find('span').text
        result_data.append(review_name)
        # print("Name",review_name)
    except:
        result_data.append('')
        # print("Name",'')

    try:
        review_location = main_review_div.find("div", {"class": "location"}).find('span').text
        result_data.append(review_location)
        # print("Location", review_location)
    except:
        result_data.append('')
        # print("Location", '')

    try:
        review_score_classes=main_score_h1.find("div", {"class": "rating"}).find('span').find('span')['class']
        score = int(review_score_classes[1].replace('bubble_',''))/10
        result_data.append(score)
        # print('Rating',score)
    except:
        result_data.append('')
        # print('Rating', '')

    try:
        review_date = main_review_div.find("span", {"class": "ratingDate relativeDate"})['title']
        result_data.append(review_date)
        print('review_date')
        # print('Rating',score)
    except:
        result_data.append('')
        # print('Rating', '')

    try:
        review_title = main_review_div.find("span", {"class": "noQuotes"}).text
        result_data.append(review_title)
        # print("Title", review_title)
    except:
        result_data.append('')
        # print("Title", '')

    try:
        review_text = main_review_div.find("p", {"class": "partial_entry"}).text
        # print(review_text)
        result_data.append(review_text)
        # print("Text", review_text)
    except:
        result_data.append('')
        # print("Text", '')

    update_csv(result_data)

# page urls
site_lists=['https://en.tripadvisor.com.hk/Attractions-g294217-Activities-c42-Hong_Kong.html',
            'https://en.tripadvisor.com.hk/Attractions-g294217-Activities-c42-oa30-Hong_Kong.html#FILTERED_LIST',
            'https://en.tripadvisor.com.hk/Attractions-g294217-Activities-c42-oa60-Hong_Kong.html#FILTERED_LIST',
            'https://en.tripadvisor.com.hk/Attractions-g294217-Activities-c42-oa90-Hong_Kong.html#FILTERED_LIST',
            'https://en.tripadvisor.com.hk/Attractions-g294217-Activities-c42-oa120-Hong_Kong.html#FILTERED_LIST',
            'https://en.tripadvisor.com.hk/Attractions-g294217-Activities-c42-oa150-Hong_Kong.html#FILTERED_LIST']
#article urls
article_urls=[]

# get all article urls
for site_list in site_lists:
    response = requests.get(site_list)
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.findAll("div", {"class": "listing_title "})
    for article in articles:
        article_urls.append('https://en.tripadvisor.com.hk'+article.find('a')['href'])

# article_urls = ['https://en.tripadvisor.com.hk/Attraction_Review-g294217-d8628344-Reviews-Hong_Kong_with_Stephen-Hong_Kong.html']

#visit all article urls
for article_url in article_urls:
    response = requests.get(article_url)
    soup = BeautifulSoup(response.content, "html.parser")

    #get review page urls
    page_numbers_div = soup.findAll("div", {"class": "pageNumbers"})
    if (len(page_numbers_div)>1):
        page_review_div=page_numbers_div[0]
        page_review_numbers=page_review_div.findAll('a')

        #get last page number of review
        page_review_last_number=int(page_review_numbers[len(page_review_numbers)-1].text)

        #create review page urls
        review_page_urls=[]
        review_page_urls.append(article_url)
        for x in range(1, page_review_last_number):
            tmp_value='or'+str(x*10)+'-'
            tmp_url=article_url.replace('-Reviews-','-Reviews-'+tmp_value)
            review_page_urls.append(tmp_url)
        print(review_page_urls)

        #get every review urls
        review_individual_urls=[]
        for review_page_url in review_page_urls:
            response_page = requests.get(review_page_url)
            soup_page = BeautifulSoup(response_page.content, "html.parser")
            review_individual_divs=soup_page.findAll("div", {"class": "review-container"})
            for review_individual_div in review_individual_divs:
                review_individual_url_tmp=review_individual_div.find("div", {"class": "quote isNew"})
                if (review_individual_url_tmp):
                    review_individual_urls.append('https://en.tripadvisor.com.hk'+review_individual_url_tmp.find('a')['href'])
                    # print('https://en.tripadvisor.com.hk'+review_individual_url_tmp.find('a')['href'])
                    get_review_content('https://en.tripadvisor.com.hk'+review_individual_url_tmp.find('a')['href'])
                else:
                    review_individual_url_tmp=review_individual_div.find("div", {"class": "quote"})
                    review_individual_urls.append('https://en.tripadvisor.com.hk'+review_individual_url_tmp.find('a')['href'])
                    # print('https://en.tripadvisor.com.hk'+review_individual_url_tmp.find('a')['href'])
                    get_review_content('https://en.tripadvisor.com.hk'+review_individual_url_tmp.find('a')['href'])

#-------------------------------------------------------------------------------------------------------------------------------------------------

