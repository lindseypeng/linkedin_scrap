from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
import numpy as np
import re
import time


driver = webdriver.Chrome(executable_path='/Users/mac/Downloads/chromedriver')

driver.get(
'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

elementID = driver.find_element_by_id('username')
elementID.send_keys("lqpeng@ualberta.ca")

elementID = driver.find_element_by_id('password')
elementID.send_keys("Woaili123")

elementID.submit()

time.sleep(20)

allinfo=[]
columns=['company_link','company_name','location','size','industry']
##linkedinjobsearch
url="https://www.linkedin.com/jobs/search/?geoId=92000000&keywords=data%20scientist&location=Worldwide"
for i in np.arange(50,975,25):
    try:
        page="&start={}".format(i)
        print(url+page)
        new_url=url+page
        #load page with selenium
        driver.get(new_url)
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
            time.sleep(5)
        ##finally we hav all postings
        

        for j in mydivs:
            try:
                company_info=[]
                get_id=j.get('id')
                xpath='//*[@id="{}"]'.format(get_id)
                ##click on page
                driver.find_element_by_xpath(xpath).click()
                time.sleep(5)
                #reload into soup again
                soup = BeautifulSoup(driver.page_source,"html.parser")
                ##now extracting all neccessary info from static page
                time.sleep(5)
                ###
                name=soup.findAll("a", 
                                  {"class":
                        "jobs-details-top-card__company-url t-black--light t-normal ember-view"})
                if len(name)==0:
                    name=soup.soup.findAll("a", 
                                  {"class":
                        "jobs-details-top-card__company-url t-black--light t-normal ember-view"})
                company_link=name[0].get('href')
                company_info.append(company_link)
                company_name=name[0].get_text().replace('\n','').strip()
                company_info.append(company_name)
                
                ##location
                location=soup.findAll("span", 
                                  {"class":
                        "jobs-details-top-card__bullet"})
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
                
                current=pd.DataFrame(allinfo,columns=columns)
                current.to_csv("/Users/mac/Desktop/linkedin_Scrap_dec20_2.csv")
                time.sleep(5)
            except:
                pass
    except:
        pass
