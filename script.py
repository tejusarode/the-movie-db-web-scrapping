import requests
from bs4 import BeautifulSoup 
import pandas as pd


response = requests.get("https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=as&searchTextText=Python%2CMumbai%2CNavi+Mumbai%2CThane&txtKeywords=Python&txtLocation=Mumbai%2CNavi+Mumbai%2CThane&cboWorkExp1=0").text
soup_data = BeautifulSoup(response,'lxml') #converting data from string to bs4

first_div = soup_data.find('li',class_='clearfix job-bx wht-shd-bx')
# print(first_div)
job_title = first_div.find('h2').text.strip()
company_name = first_div.find('h3',class_="joblist-comp-name").text.strip().replace("(More Jobs)","")
experience = first_div.find('li').text.replace('card_travel','')
first_ul = first_div.find('ul',class_='top-jd-dtl clearfix')
all_li = first_ul.find_all('li')
package_li = all_li[1].text
location = all_li[2].text.strip().replace('location_on','').strip()

job_desc_ul = first_div.find('ul',class_='list-job-dtl clearfix')
jd = job_desc_ul.find('li').text.strip()
key_skills = job_desc_ul.find('span',class_='srp-skills').text.strip()
# print(key_skills)

first_job_info = {
    'Job-Title' : job_title,
    'Company-Name':company_name,
    'Experience':experience,
    'Package':package_li,
    'Location':location,
    'JD':jd,
    'Key-Skills':key_skills
}

lst = []
lst.append(first_job_info)

df = pd.DataFrame(lst)
df.to_excel('first-job.xlsx')
