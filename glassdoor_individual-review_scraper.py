#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 21:00:25 2022

@author: jjensen001
"""


# importing necessary packages
# import re
from bs4 import BeautifulSoup
# import xlsxwriter
import pandas as pd
from selenium import webdriver
# from selenium.webdriver.support.select import Select
import time
# from selenium.webdriver.common.keys import Keys
import math


# login to glassdoor here
driver = webdriver.Firefox(executable_path='C:/Users/user/Documents/folder/geckodriver')

# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.glassdoor.com/index.htm')
time.sleep(3)

# locate sign_in button by_class_name
signin_button = driver.find_element_by_class_name('d-none.d-lg-block.p-0.LockedHomeHeaderStyles__signInButton')

# .click() to mimic button click
signin_button.click()
time.sleep(3)

# locate email form by_class_name
username = driver.find_element_by_id('modalUserEmail')

# send_keys() to simulate key strokes
username.send_keys('username@email.com')
time.sleep(3)

# locate password form by_class_name
password = driver.find_element_by_id('modalUserPassword')

# send_keys() to simulate key strokes
password.send_keys('password')
time.sleep(3)

# locate submit button by_class_name
log_in_button = driver.find_element_by_name('submit')

# .click() to mimic button click
log_in_button.click()
time.sleep(3)


# Load company gd page
driver.get('https://www.glassdoor.com/Reviews/Generic-Company-Reviews-E33373.htm')
time.sleep(3)

# max_pages function by locating just the number of total reviews divided by 10 reviews per page
rv_count_pre = driver.find_element_by_class_name('paginationFooter')
max_pages = math.ceil(float(rv_count_pre.text[-11:-8])/10)

    
# create empty list 
reviews_list = []
  
# iterate through all pages and load scraped data for all individual review fields
for page in range(1, max_pages, 1):    
    page_url = 'https://www.glassdoor.com/Reviews/Generic-Company-Reviews-E33373_P'+str(page)+'.htm?sort.sortType=RD&sort.ascending=false&filter.iso3Language=eng'
    driver.get(page_url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    time.sleep(3)

    # click on 'continue reading' button for any reviews that have more review data that is not visible; usually it's advice to mngmt
    cont = driver.find_elements_by_class_name('v2__EIReviewDetailsV2__continueReading.v2__EIReviewDetailsV2__clickable.v2__EIReviewDetailsV2__newUiCta.mb')
    for x in range(0,len(cont)):
        if cont[x].is_displayed():
            cont[x].click()
    
    time.sleep(3)
    # this is the review container that contains all of the review elements
    reviews = driver.find_elements_by_class_name('gdReview')
    time.sleep(1)
    
    for review in reviews:
        rating = review.find_element_by_class_name("ratingNumber.mr-xsm").text
        pros = review.find_element_by_xpath('.//div[2]/div/div[2]/div[1]/p[2]/span').text
        cons = review.find_element_by_xpath('.//div[2]/div/div[2]/div[2]/p[2]/span').text
        emps_tenure = review.find_element_by_class_name("pt-xsm.pt-md-0.css-1qxtz39.eg4psks0").text
        if ", " in emps_tenure:
            emps_t = emps_tenure.split(', ')
            emps = emps_t[0]
            tenure = emps_t[1]
        else:
            emps = emps_tenure
            tenure = ''
        subject = review.find_element_by_class_name("reviewLink").text
        date_job_city_state = review.find_element_by_class_name("common__EiReviewDetailsStyle__newUiJobLine").text
        if " - " in date_job_city_state:
            d_j_c_s = date_job_city_state.split(' - ')
            date = d_j_c_s[0]
            j_c_s = d_j_c_s[1]
            if " in " in j_c_s:
                j_c_s_ = j_c_s.split(' in ')
                job = j_c_s_[0]
                city_state = j_c_s_[1]
                if ', ' in city_state:
                    c_y = city_state.split(', ')
                    city = c_y[0]
                    state = c_y[1]
                else:
                    city = city_state
                    state = ''
            else:
                job = j_c_s
                city = ''
                state = ''
        else:
            date = date_job_city_state
            job = ''
            city = ''
            state = ''
        advtm = review.find_elements_by_xpath('.//div[2]/div/div[2]/div[3]/p[2]/span') #note that he was able to find this via the full xpath and then adjusting the xpath hierarchy; you will need to review xpath hiearchy and understand it to fully utilize.
        if len(advtm) == 1:
            advtm = advtm[0].text
        else:
            advtm = ''
        # load all of the scraped data into a dict
        review_item = {
                'date': date,
                'rating': rating,
                'emps': emps,
                'tenure': tenure,
                'subject': subject,
                'job': job,
                'city': city,
                'state': state,
                'pros': pros,
                'cons': cons,
                'advtm': advtm}
    
        
        reviews_list.append(review_item)

# load data into a pandas data frame and then load into csv
df = pd.DataFrame(reviews_list)
print(df)
df.to_csv('C:/Users/user/Documents/Utilities/glassdoor_reviews.csv')


    
