#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 10:21:08 2020

@author: mac
"""
/Users/mac/Downloads/linkedin_test.py
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
import numpy as np
import re
import time
import random


driver = webdriver.Chrome(executable_path='/Users/mac/Downloads/chromedriver')

driver.get(
'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

elementID = driver.find_element_by_id('username')
elementID.send_keys("lqpeng@ualberta.ca")

elementID = driver.find_element_by_id('password')
elementID.send_keys("Woaili123")

elementID.submit()

time.sleep(10)


columns=['company_link','company_name','location','size','industry']
##linkedinjobsearch
url="https://www.linkedin.com/jobs/search/?geoId=92000000&keywords=data%20scientist&location=Worldwide"
for i in np.arange(75,975,25):
        page="&start={}".format(i)
        print(url+page)
        new_url=url+page
        #load page with selenium
        driver.get(new_url)
        time.sleep(random.randint(5,15))
        #load static content with soup from selenium
        soup = BeautifulSoup(driver.page_source,"html.parser")
        #get all 
        mydivs = soup.findAll("a", {"class": 
        "disabled ember-view job-card-container__link job-card-list__title"})
        ##get to the bottom of the page....slowly..
        while len(mydivs)<25:
            get_id=mydivs[-1].get('id')
            xpath='//*[@id="{}"]'.format(get_id)
            driver.find_element_by_xpath(xpath).click()
            soup = BeautifulSoup(driver.page_source,"html.parser")
            mydivs = soup.findAll("a", {"class": 
        "disabled ember-view job-card-container__link job-card-list__title"})
            time.sleep(random.randint(2,10))
        ##finally we hav all postings
        print('all_job_loaded at page {}'.format(i))
        allinfo=[]
        for idx, j in enumerate(mydivs):
            print("this is posting {} at page {}".format(idx,i))
            try:
                company_info=[]
                get_id=j.get('id')
                xpath='//*[@id="{}"]'.format(get_id)
                ##click on page
                driver.find_element_by_xpath(xpath).click()
                time.sleep(random.randint(5,10))
                #reload into soup again
                soup = BeautifulSoup(driver.page_source,"html.parser")
                ##now extracting all neccessary info from static page
                #time.sleep(random.randint(5,15))
                ###
                name=soup.findAll("a", 
                                  {"class":
                        "jobs-details-top-card__company-url t-black--light t-normal ember-view"})
    
                company_link=name[0].get('href')
                company_info.append(company_link)
                company_name=name[0].get_text().replace('\n','').strip()
                company_info.append(company_name)
                print("company_name: {}".format(company_name))
                ##location is trickier: 2 type of choices
                location=soup.findAll("a", 
                                  {"class":
                        "jobs-details-top-card__exact-location t-black--light link-without-visited-state"})
                if len(location)==0:
                    location=soup.findAll("span", 
                                  {"class":
                        "jobs-details-top-card__bullet"})
                    location=location[0].get_text().replace('\n','').strip()
                else: 
                    location=location[0].get_text().replace('\n','').strip()
                company_info.append(location)
                #employee number and industry
                employees_industry=soup.findAll("span", 
                                  {"class":
                        "jobs-details-job-summary__text--ellipsis"})
                
                employees=employees_industry[2].get_text().replace('\n','').strip()
                industry=employees_industry[3].get_text().replace('\n','').strip()
                company_info.append(employees)
                company_info.append(industry)
                
                allinfo.append(company_info)
                print("allinfo length is {}".format(len(allinfo)))
                current=pd.DataFrame(allinfo,columns=columns)
                current.to_csv("/Users/mac/Desktop/linkedin_Scrap_dec20_{}.csv".format(i))
                print("saved to linkedin_Scrap_dec20_{}.csv".format(i))
                print("allinfo length is {}".format(len(current)))
                time.sleep(random.randint(5,10))
                
            except:
                pass
            #time.sleep(i)
            time.sleep(random.randint(10,30))
