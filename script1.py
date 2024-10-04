import requests
from bs4 import BeautifulSoup 
import pandas as pd
response = requests.get("https://www.themoviedb.org/movie?page=1").text
# print(response)
soup_data = BeautifulSoup(response,'lxml')
# print(soup_data)

first_div=soup_data.find('div',class_='card style_1')
# print(first_div)

inner_div=first_div.find('div',class_='content')
first_h2=inner_div.find('h2')
movie_name=first_h2.find('a').text
# print(movie_name)

rel_date=inner_div.find('p').text
# print(rel_date)

rating_div=inner_div.find('div',class_="user_score_chart 5de6f6133faba00015133c4d")
rating = rating_div['data-percent'] 
# print(rating["data-percent"])
# print(rating)



url1=inner_div.find('a')
base_url="https://www.themoviedb.org/movie?page=1"
final_url=base_url.replace('/movie',url1['href'])
# print(final_url)
#               or
# inner_link=inner_div.find('a')['href']
# inner_link=base_url+inner_link


resp2=requests.get(final_url).text
soup_data2=BeautifulSoup(resp2,'lxml')
# print(soup_data2)

genre_class=soup_data2.find('span',class_="genres")
genre = genre_class.findAll('a')
genre_list = [gen.text for gen in genre] 
genres = ', '.join(genre_list).strip()
print(genres)

run_time=soup_data2.find('span',class_='runtime').text.strip()
# print(run_time)

ovrw_div=soup_data2.find('div',class_='overview')
overview=ovrw_div.find('p').text
# print(overview)

ol_profile=soup_data2.find('ol',class_='people no_image')
if ol_profile is not None:
    all_li=ol_profile.find_all('li')
    director=all_li[2].text.strip().replace('Director','')
    # print(director)


first_movie_data = {
    'Movie Name' : movie_name,
    'Release Date':rel_date,
    'Rating':rating,
    'Director':director,
    'Run Time':run_time,
    'Genre':genres,
    'Overview':overview
}

# print(first_movie_data)
# lst = []
# lst.append(first_movie_data)

# df = pd.DataFrame(lst)
# df.to_excel('first-movie-data.xlsx')


         
