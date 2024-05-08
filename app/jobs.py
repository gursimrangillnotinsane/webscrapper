

from collections import defaultdict
import urllib.request
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
from urllib.request import Request, urlopen
import time
import re
from datetime import datetime
from selenium_stealth import stealth
import random
from webdriver_manager.chrome import ChromeDriverManager

indeed_posts=[]
# CANADIAN BANK
###
#
#
#
headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'}

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument(f"user-agent={headers}")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

# a function to check if there is a website in next page
def isThereSite(url):
        headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'}
        req = urllib.request.Request(url,headers=headers)
        #to advoid sending too many requests at one time
        time.sleep(1)
        webUrl = urlopen(req)
        html=webUrl.read()
        # Scrapping the Web
        soup = BeautifulSoup(html, 'html.parser')
       
        # Outer Most Entry Point of HTML:
        if soup.find('div',{'class':'noResults'}) :
                return False
        return True

def isThereASiteIndeed(url):
              
                driver.get(url)
                html=driver.page_source
                # Scrapping the Web (you can use 'html' or 'lxml')
                soup = BeautifulSoup(html, 'html.parser')
            
                # Outer Most Entry Point of HTML:
                if soup.find('div',id='mosaic-provider-jobcards'):
                    return True
                return False

def isThereASiteLinkdin(url):
               
                driver.get(url)
                html=driver.page_source
                # Scrapping the Web (you can use 'html' or 'lxml')
                soup = BeautifulSoup(html, 'html.parser')
            
                # Outer Most Entry Point of HTML:
                if soup.find('li'):
                    return True
                return False

# a function to srap a website which take skill, place, sortBy and sheet number as argument
def searchJobsJobBank(skill, place,page):
        jobbankList=[]
   
        maxPage=page+5
        # a boolean if there is a next page, it is true otherwise false
        nextPage=True
        #printing the current skill we are looking for
        print(skill)
        #a loop which ends when there are no next page 
        while nextPage:
                if page==maxPage:
                        break
               #default header
                headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko)         Chrome/92.0.4515.107 Mobile Safari/537.36'}

                #url of canadian bank jobs which take skill as the searchstring and pagenumber as page a well as place
                url="https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring="+skill+"&page="+str(page)+"&locationstring="+place+"&sort=D";
                #printing the number of page we are scannign on
                print("Scanning the "+ str(page)+" page")
               
                # scrapping the website in try block if the website is down 
                try:
                    req = urllib.request.Request(url,headers=headers)
                    webUrl = urlopen(req)
                except Exception  as e:
                    print("Error:", e)
                
                #reading the html
                html=webUrl.read()

                # Scrapping the Web 
                soup = BeautifulSoup(html, 'html.parser')

                # Outer Most Entry Point of HTML:
                outer_most_point=soup.find('div',id='ajaxupdateform:result_block')

                # lists where the data are stored:
                company=[]
                jobs=[]
                links=[]
                salary=[]
                post_date=[]

                
                #all the jobs are in article 
                if outer_most_point is not None and isinstance(outer_most_point, bs4.element.Tag):
                        list_items = outer_most_point.find_all('article')
                for i in list_items: 
                
                                # Job Title:
                                
                                if i.find('span',{'class':'noctitle'}) != None:
                                        jobs=i.find('span',{'class':'noctitle'}).text.strip()
                                        if "\n" in jobs:
                                                index=jobs.index("\n")
                                                jobs=jobs[:index]
                                else:
                                        jobs="Can't retrieve the value"
                                                        
                                        
                                        
                                # Company Name:
                                if i.find('li',{'class':'business'}) != None:
                                        company=i.find('li',{'class':'business'}).text.strip()
                                        
                                else:
                                        jobs="Can't retrieve the value"
                                        
                                # Links: these Href links will take us to full job description
                                if  i.find('a',{'class':'resultJobItem'})!=None:
                                        links="https://www.jobbank.gc.ca"+ i.find('a',{'class':'resultJobItem'})['href']
                                else:
                                        jobs="Can't retrieve the value"                             
                                        
                                # Salary if available:
                                if i.find('li',{'class':'salary'}) !=None and i.find('li',{'class':'salary'}).text.strip()!="Salary not available":
                                        # a regex to find the salary
                                        salary=i.find('li',{'class':'salary'}).text.strip()
                                        payPattern=re.compile(r"\d{1,3}[,.]\d{1,3}")
                                        payMatcher=payPattern.search(salary)
                                        
                                        if payMatcher!= None:
                                                pay=payMatcher.group()
                                                salary=pay.replace(',', '')
                                        else:
                                                salary='No Salary available'
                                
                                else:
                                        salary='No Salary available'

                                # Job Post Date:
                                if i.find('li', attrs={'class': 'date'}) != None:
                                        post_date = i.find('li', attrs={'class': 'date'}).text.strip()
                                        #post_date = datetime.datetime(date[-4:]
                                else:
                                        jobs="Can't retrieve the value"
                                
                                # Put everything together in a list of lists for the default dictionary
                                jobbankList.append([company,jobs,links,salary, post_date])
            #incrementing the pagenumber
                page=page+1
            #checking if there is a next page
                nextPage=isThereSite(url)
        return jobbankList

def searchJobIndeed(skill,place,page):
    # this was used for the person contacting me who had these details for their system
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'}

    maxPage=page+50
    indeedList=[]
    nextPage=True
        #printing the current skill we are looking for
        #a loop which ends when there are no next page 
    while nextPage:      
                if page==maxPage:
                        break
            # Connecting to  Indeed
                
                url = 'https://ca.indeed.com/jobs?q=' + skill + '&l=' + place + '&sort=date' +'&start='+ str(page)
                print(url)
                #url="https://ca.indeed.com/jobs?q=programming&l=Bradford%2C+ON&from=searchOnHP&vjk=41b3ffa913ed4dc6"
            
                driver.get(url)
                html=driver.page_source
                # Scrapping the Web (you can use 'html' or 'lxml')
                soup = BeautifulSoup(html, 'html.parser')
               
                # Outer Most Entry Point of HTML:
                outer_most_point=soup.find('div',id='mosaic-provider-jobcards')

                # "UL" lists where the data are stored:
                company=[]
                jobs=[]
                links=[]
                salary=[]
                post_date=[]
               
                if outer_most_point is not None and isinstance(outer_most_point, bs4.element.Tag):
                        list_items = outer_most_point.find_all('li')
                        print(len(list_items))
    # Continue processing the data
                        for i in list_items:
                               
                                # Job Title:
                                job_title=i.find('h2',{'class':"jobTitle css-14z7akl eu4oa1w0"})
                                if job_title != None:
                                        jobs=job_title.find('a').text
                                        
                                # Company Name:

                                if i.find('span',{'class':'css-92r8pb eu4oa1w0'}) != None:
                                        company=i.find('span',{'class':'css-92r8pb eu4oa1w0'}).text   
                                        
                                # Links: these Href links will take us to full job description
                                if  i.find('a',{'class':'jcs-JobTitle css-jspxzf eu4oa1w0'})!=None:
                                        links="https://indeed.com"+i.find('a',{'class':'jcs-JobTitle css-jspxzf eu4oa1w0'})['href']
                                        
                                # Salary if available:
                                if i.find('div',{'class':'css-1cvo3fd eu4oa1w0'}) != None:
                                        salary=i.find('div',{'class':'css-1cvo3fd eu4oa1w0'}).text

                                else:
                                        salary='No Salary'

                                # Job Post Date:

                                if i.find('span', attrs={'class': 'css-qvloho eu4oa1w0'}) != None:
                                        post_date = i.find('span', attrs={'class': 'css-qvloho eu4oa1w0'}).text

                                # Put everything together in a list of lists for the default dictionary
                                        
                                indeedList.append([company,jobs,links,salary, post_date])
                        
                page=page+10
                #checking if there is a next page
                nextPage=isThereASiteIndeed(url)
    return indeedList


def searchJobsLinkdin(skill,place,page):
    # this was used for the person contacting me who had these details for their system
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'}

   
    linkdinlist=[]
    nextPage=True
    maxPage=page+5
        #printing the current skill we are looking for
        #a loop which ends when there are no next page 
    while nextPage:      
                if page==maxPage:
                        break
                url =" https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords="+skill+"&location="+place+"&start="+str(page)
                print(url)
                #url="https://www.linkedin.com/jobs/search/?currentJobId=3899546145&geoId=105149290&keywords=programming&location=Ontario%2C%20Canada&origin=JOBS_HOME_SEARCH_BUTTON&refresh=true"
                #url="https://ca.indeed.com/jobs?q=programming&l=Bradford%2C+ON&from=searchOnHP&vjk=41b3ffa913ed4dc6"
               
                driver.get(url)
                html=driver.page_source
                # Scrapping the Web (you can use 'html' or 'lxml')
                soup = BeautifulSoup(html, 'html.parser')
            
                # Outer Most Entry Point of HTML:
                outer_most_point=soup.find('body')
            
                # "UL" lists where the data are stored:
                company=[]
                jobs=[]
                links=[]
                salary=[]
                post_date=[]
                if outer_most_point is not None and isinstance(outer_most_point, bs4.element.Tag):
                        list_items = outer_most_point.find_all('li')

                for i in list_items:
                # Job Title:
                    job_title=i.find('h3',{'class':"base-search-card__title"})
                    if job_title != None:
                        jobs=job_title.text.strip("\n").strip()
                # Company Name:

                    if i.find('h4',{'class':'base-search-card__subtitle'}) != None:
                        company=i.find('h4',{'class':'base-search-card__subtitle'}).text.strip("\n").strip()
                        
                # Links: these Href links will take us to full job description
                    if  i.find('a',{'class':'base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]'})!=None:
                        links=i.find('a',{'class':'base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]'})['href']
                        
                # Salary if available:
                    if i.find('div',{'class':'css-1cvo3fd eu4oa1w0'}) != None:
                        salary=i.find('div',{'class':'css-1cvo3fd eu4oa1w0'}).text

                    else:
                        salary='No Salary'

                # Job Post Date:

                    if i.find('span', attrs={'class': 'job-search-card__location'}) != None:
                        post_date = i.find('span', attrs={'class': 'job-search-card__location'}).text.strip("\n").strip()

                # Put everything together in a list of lists for the default dictionary
                                
                    linkdinlist.append([company,jobs,links,salary, post_date])
                page=page+1
                  #checking if there is a next page
                nextPage=isThereASiteLinkdin(url)
    return linkdinlist

