import requests
from bs4 import BeautifulSoup 
import pandas as pd

lst=[]
response = requests.get("https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=as&searchTextText=Python%2CMumbai%2CNavi+Mumbai%2CThane&txtKeywords=Python&txtLocation=Mumbai%2CNavi+Mumbai%2CThane&cboWorkExp1=0").text
soup_data = BeautifulSoup(response,'lxml') #converting data from string to bs4
all_div = soup_data.find_all('li',class_='clearfix job-bx wht-shd-bx')
for item in all_div:
    job_title = item.find('h2').text.strip()
    company_name = item.find('h3',class_="joblist-comp-name").text.strip().replace("(More Jobs)","")
    experience = item.find('li').text.replace('card_travel','')
    first_ul = item.find('ul',class_='top-jd-dtl clearfix')
    all_li = first_ul.find_all('li')
    if len(all_li)<3:
        package_li = "NA"
    else:
        package_li = all_li[1].text

    if len(all_li)<3:
        location = all_li[1].text.strip().replace('location_on','').strip()
    else:
        location = all_li[2].text.strip().replace('location_on','').strip()

    job_desc_ul = item.find('ul',class_='list-job-dtl clearfix')
    jd = job_desc_ul.find('li').text.strip()
    key_skills = job_desc_ul.find('span',class_='srp-skills').text.strip()
    
    all_job_info = {
    'Job-Title' : job_title,
    'Company-Name':company_name,
    'Experience':experience,
    'Package':package_li,
    'Location':location,
    'JD':jd,
    'Key-Skills':key_skills
    }
    
    # print(all_job_info)
    lst.append(all_job_info)

df = pd.DataFrame(lst)
df.to_excel('all-job.xlsx')