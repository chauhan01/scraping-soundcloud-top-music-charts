
#Importing libraries
from selenium import webdriver 
import pandas as pd  
from selenium.webdriver.common.keys import Keys
import time


driver = webdriver.Chrome()



driver.get("https://soundcloud.com/charts/top?genre=all-music") 

driver.find_element_by_css_selector("#content > div > div.l-fluid-fixed > div.sc-border-light-right.l-main > div.l-content > div > div.chartsMain__filters > div:nth-child(3) > button").click()



dropdown = driver.find_elements_by_xpath("//section[2]//ul//*[@class = 'sc-link-dark sc-truncate g-block']")



genres = []
links = []
for i in dropdown:
    genre = i.text
    link = i.get_attribute('href')
    genres.append(genre)
    links.append(link)



link_data = pd.DataFrame({"Genre": genres, "Link":links})
link_data.head()


def scrap(link_df):
    
    
    df = pd.DataFrame(columns = ['song_title', 'rank', 'genre', 'artist', 'this_week_score', 'total_score'])
    
    for index, row in link_df.iterrows():
        genre = row.Genre
        link = row.Link
        
        driver.get(link) 
    
        time.sleep(5)
        elem = driver.find_element_by_tag_name("body")
        no_of_pagedowns = 8

        while no_of_pagedowns:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            no_of_pagedowns-=1
    
        #song title and artist name
        song_data_scrap = driver.find_elements_by_class_name("chartTrack__details")
    
        # song total play counts and this week play counts
        song_score_scrap = driver.find_elements_by_class_name("chartTrack__score")
    
        # creating empty lists for storing scraped data
        song_data = []
        song_score = []
    
    
        for i in song_data_scrap:
            song_data.append(i.text)
        
    
        for i in song_score_scrap:
            song_score.append(i.text)
    

        # song genre
        song_genre = [genre for i in range(50)]
    
        #song rank
        rank = list(range(1, 51))
    
        #artist name
        artist = [i.split('\n')[0] for i in song_data]
    
        #song title
        title = [i.split('\n')[1] for i in song_data]
    
        #this week score
        score_this_week = []
        for i in song_score:
            if len(i) < 5:
                score = 0
            else:
                score = i.split()[0]
            score_this_week.append(score)
    
        # total score
        total_score = []
        for i in song_score:
            if len(i) < 5:
                score = 0
            else:
                score = i.split()[3]
            total_score.append(score)
            
            
        
        temp_df = pd.DataFrame({"song_title": title, "rank":rank, "genre":genre, "artist": artist, "this_week_score": score_this_week, "total_score":total_score})
        df = df.append(temp_df, ignore_index=True)
        print('dataframe shape is ',df.shape)   
         
    return df


# calling the function and creating the final dataframe
data = scrap(link_data)




