import requests
from bs4 import BeautifulSoup 
import pandas as pd
import re
response = requests.get("https://www.themoviedb.org/movie?page=1").text

soup_data = BeautifulSoup(response,'lxml')

all_div = soup_data.find_all('div', class_='card style_1')
page_1_data=[]
for item in all_div:
    inner_div = item.find('div', class_='content')
    first_h2 = inner_div.find('h2')
    movie_name = first_h2.find('a').text
    # print(movie_name)
    rel_date=inner_div.find('p').text
    # print(rel_date)
    rating_div=inner_div.find_all(re.compile('div'),class_="user_score_chart")    
    for rating_divs in rating_div:
        if 'data-percent' in rating_divs.attrs:
            rating = rating_divs['data-percent']
            # print(rating)
    url1=inner_div.find('a')
    url="https://www.themoviedb.org/movie?page=1"
    final_url=url.replace('/movie',url1['href'])
    # print(final_url)
    resp2=requests.get(final_url).text
    soup_data2=BeautifulSoup(resp2,'lxml')
    genre_class=soup_data2.find('span',class_="genres")
    genre = soup_data2.findAll('span', class_='genres')
    genre_list = [gen.text for gen in genre]  
    genres = ', '.join(genre_list).strip()
    # print(genres)
    run_time_find=soup_data2.find('span',class_='runtime')
    if run_time_find:
        run_time_list=[rt.text.strip() for rt in run_time_find]
    else:
        print("N/a")
    run_time="\n".join(run_time_list)
    # print(run_time)
    ovrw_div=soup_data2.find('div',class_='overview')
    ovrw=ovrw_div.find('p')
    if ovrw:
        ovrw_list=[ovrw_text.text for ovrw_text in ovrw]
    overview='\n'.join(ovrw_list)
    # print(overview)
    ol_profile=soup_data2.find('ol',class_='people no_image')
    if ol_profile is not None:
        all_li=ol_profile.find_all('li')
        for li in all_li:
            if "Director" in li.text:
                director = re.sub(r'Director|Writer|Screenplay|Story|,', '', li.text.strip())
                # print(director)
    first_page_data={
    'Movie Name' : movie_name,
    'Release Date':rel_date,
    'Rating':rating,
    'Director':director,
    'Run Time':run_time,
    'Genre':genres,
    'Overview':overview
    }
    # print(first_page_data)
    page_1_data.append(first_page_data)
    # print(page_1_data)

df = pd.DataFrame(page_1_data)
df.to_excel('page-1.xlsx', index=False)


