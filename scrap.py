# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from time import sleep
from tabulate import tabulate
'''
   Currently supports:  #star-movies
            #sony-max
            #movies-now
            #romedy-now
            #movies-ok
            #sony-pix
            #hbo
            #filmy
            #star-gold
'''

web_url = "http://tvinfo.in/"
web_url2= "http://tvscheduleindia.com/channel/"
web_url3="http://tvscheduleindia.com"
base_url = 'http://www.imdb.com/find?q='


class Movie_entry:
    movie_name =''
    movie_start=''
    movie_end=''
    movie_rating=0
    movie_channel=''
    movie_date=''

    def get_rating(self ):
        try:
            print "Checking IMDb rating of "+ self.movie_name
            movie_search = '+'.join(self.movie_name.split())
            movie_url = base_url + movie_search + '&s=all'
            print(movie_url)
            br = Browser()
            br.open(movie_url)
            link = br.find_link(url_regex=re.compile(r'/title/tt.*'))
            res = br.follow_link(link)
            soup = BeautifulSoup(res.read(), "lxml")
            movie_title = soup.find('title').contents[0]
            rate = soup.find('span', itemprop='ratingValue')
            if rate is not None:
                self.movie_rating=rate

        except:
            self.movie_rating='-'

movies_of_my_genre=[]



#Method to initialize pdf object
"""
def pdf_save(data_movies,headers):
    pdf = fpdf.FPDF(format='letter')
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Tv Timings !",ln=1, align="C")
    #pdf.cell(200, 10, str(tabulate(data_movies,headers)),0,1, align="l")
    for data in data_movies:
        str1 = "Movie: " + str(data[0]) + "  Time: " + str(data[1])+ "  Rating: " + str(data[2])
        pdf.cell(200, 10, str1,0,1, align="l")
    pdf.output('La-Z-Boy.pdf')

"""

def getBSoup(url):
    print'''
Processing...

    '''
    print url
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "lxml")
    return soup



### def search_channel(channel,channel2):
def search_channel(channel2):
    # channel_url = web_url + channel + ".html"
    # soup = getBSoup(channel_url)
    time = []
    ratings = []
    #title_search = re.compile('/title/tt\d+')

    # movie_name = soup.find_all('p', {"class": "title2"})

    channel2_url = web_url2 + channel2
    soup2 = getBSoup(channel2_url)
    #print(soup2.prettify())
    
    
    #print(movie_data1)
    movie_list = []
    movie_name = ""
    movie_time = ""
    movie_genre = ""
    movie_length = ""
    movie_rating = ""
    movies_list2 = []
    for i in soup2.find_all('tr'):
        cnt=0
        for j in i.find_all('td'):
            cnt+=1
            print " ".join(j.text.split())
            print cnt
            if cnt==2:
                movie_name = " ".join(j.text.split())
            elif cnt==3:
                movie_time = " ".join(j.text.split())
            elif cnt==4:
                movie_genre = " ".join(j.text.split())
            elif cnt==5:
                movie_length = " ".join(j.text.split())
        print "movie_name  "+movie_name
        if movie_name!="":    
            link = "https://www.google.co.in/search?client=ubuntu&channel=fs&q="
            search_string = movie_name+" movie Imdb rating"
            search_string = "-".join(search_string.split())
            google_search = link+search_string
            print google_search
            r = requests.get(google_search)
            soup = BeautifulSoup(r.text,"html.parser")
            #print soup.find('cite').text
            movie_rating_link = soup.find('cite').text
            
            movie_rating_link = "http://"+movie_rating_link
            print movie_rating_link
            r = requests.get(movie_rating_link)
            soup = BeautifulSoup(r.text,"html.parser")
            rate = soup.find('span', itemprop='ratingValue')
            if rate is not None:
                movie_rating = rate.text
            else:
                movie_rating = "-"

            movies_list1 = [movie_name,movie_time,movie_genre,movie_length,movie_rating]

            movies_list2.append(movies_list1)
            movie_dict = {
                    'movie_name':movie_name,
                    'movie_time':movie_time,
                    'movie_genre':movie_genre,
                    'movie_length':movie_length,
                    'movie_rating':movie_rating
                }
            movie_list.append(movie_dict)
            
    #print movie_list

    headers = ['Movie Name','Movie Timing','Movie Genre', 'Movie Length','Movie Rating']
    print tabulate(movies_list2, headers = headers)

            
        

    

def genre_recommend(genre):
    genre=genre.lower()
    r = requests.get(web_url3)
    soup3=BeautifulSoup(r.content,"html.parser")
    movies_list2 = []
    cntr = 0
    for row in soup3.find_all('div',{'class' : 'col-1 channel_card' }):

        col = row.find('a')
        print col['href']
        channel_link = web_url3 + col['href']
        channel_name = col['href']
        channel_name = channel_name.strip('/channel/')
        print channel_name
        r = requests.get(channel_link)
        soup = BeautifulSoup(r.content,"html.parser")
        movie_list = []
        movie_name = ""
        movie_time = ""
        movie_genre = ""
        movie_length = ""
        movie_rating = ""
        cntr+=1
        
        for i in soup.find_all('tr'):
            cnt=0
            for j in i.find_all('td'):
                cnt+=1
                print " ".join(j.text.split())
                print cnt
                if cnt==2:
                    movie_name = " ".join(j.text.split())
                elif cnt==3:
                    movie_time = " ".join(j.text.split())
                elif cnt==4:
                    movie_genre = " ".join(j.text.split())
                elif cnt==5:
                    movie_length = " ".join(j.text.split())
            print "movie_name  "+movie_name
            movie_genre = movie_genre.strip().lower()
            if movie_name!="" and movie_genre==genre:    
                link = "https://www.google.co.in/search?client=ubuntu&channel=fs&q="
                search_string = movie_name+" movie Imdb rating"
                search_string = "-".join(search_string.split())
                google_search = link+search_string
                print google_search
                r = requests.get(google_search)
                soup = BeautifulSoup(r.text,"html.parser")
                #print soup.find('cite').text
                movie_rating_link = soup.find('cite').text
                
                movie_rating_link = "http://"+movie_rating_link
                print movie_rating_link
                r = requests.get(movie_rating_link)
                soup = BeautifulSoup(r.text,"html.parser")
                rate = soup.find('span', itemprop='ratingValue')
                if rate is not None:
                    movie_rating = rate.text
                else:
                    movie_rating = "-"

                movies_list1 = [movie_name,movie_time,movie_genre,movie_length,movie_rating,channel_name]

                movies_list2.append(movies_list1)
                movie_dict = {
                        'movie_name':movie_name,
                        'movie_time':movie_time,
                        'movie_genre':movie_genre,
                        'movie_length':movie_length,
                        'movie_rating':movie_rating,
                        'channel_name':channel_name
                    }
                movie_list.append(movie_dict)

    headers = ['Movie Name','Movie Timing','Movie Genre', 'Movie Length','Movie Rating','Channel Name']
    print tabulate(movies_list2, headers = headers)




    """
    for row in islice(soup4.findAll('a'),int(no_of_channel)):                          # This decides how many channels to see (here 10)
        channel_name= row.find('span').text.replace('\n','')
        print 'Searching in  :' + channel_name
        soup5=getBSoup2(web_url3 + row.get('href'))
        soup5=soup5.find('div',{'class': 'resultCont'})
        soup5 = soup5.findAll('tr')
        soup5=soup5[:-1]
        for link in soup5:                                           # link contains code of <tr>
            if(link.find('b',{'class':'genre'})):
                mov_gen=link.find('b',{'class':'genre'}).string.lower()
                mov_gen = re.sub('[' + string.punctuation + ']', ' ', mov_gen)
                mov_gen=mov_gen.split( )
                if genre in mov_gen:
                    date=link.find('span',{'class':'date'}).string.replace(" ", "").replace("\n", "")
                    if (date == "Today"):
                        new_movie=Movie_entry()
                        new_movie.movie_name=link.find('strong').string.replace("\n", "")
                        new_movie.movie_start=link.find('b',{'class':'from'}).string
                        new_movie.movie_end=link.find('b',{'class':'to'}).string
                        new_movie.movie_channel= channel_name
                        movies_of_my_genre.append(new_movie)
        """
"""
def get_ratings(movies_of_my_genre):
    for movie in movies_of_my_genre:
        try:
            print "Checking IMDb rating of :   " + movie.movie_name.replace('\t','')
            movie_search = '+'.join(movie.movie_name.split())
            movie_url = base_url + movie_search + '&s=all'
            br = Browser()
            br.open(movie_url)
            link = br.find_link(url_regex=re.compile(r'/title/tt.*'))
            res = br.follow_link(link)
            soup = BeautifulSoup(res.read(), "lxml")
            movie_title = soup.find('title').contents[0]
            rate = soup.find('span', itemprop='ratingValue')
            if rate is not None:
                movie.movie_rating=float(rate.contents[0])
            else:
                movie.movie_rating=0
        except:
            movie.movie_rating = 0"""

def main():

    print'''
                                                                        Welcome to Movie Rating Project
                                                                    For the love of good content
    '''
    print("If you want to check movies movies on a channel select 1")
    print("To get movies of a specific Genre select 2")
    choice=raw_input("Enter choice: ")

    if(str(choice)=='1'):
        #channel = raw_input("Enter name of the TV Channel: ")
        channel2 = raw_input("Enter name of the TV Channel: ")
        #channel = "-".join([item.strip() for item in channel.split(" ")])
        if(len(channel2.split())>1):
            channel2 = "-".join([item.strip() for item in channel2.split(" ")])
            channel2 = channel2.upper()
        else:
            channel2 = channel2.strip()
            channel2 = channel2.upper()
        movie_rating = search_channel(channel2)
    else:
        genre = raw_input("Enter Genre: (like  comedy, action ....) ")
        #no_of_channel = raw_input("Enter No of channels to check (e.g, 1-44)")
        genre_recommend(genre)
        """
        print '\nNumber of movies of genre ' + genre.upper()+' found : ' + str(len(movies_of_my_genre))
        get_ratings(movies_of_my_genre)
        sorted_list = sorted(movies_of_my_genre, key=lambda movie: movie.movie_rating, reverse=True)

        headers = ['Movies','Channel','Time', 'Rating']
        data_movies2 = []

        for movie in islice(sorted_list, 5):
            data_movies2.append([movie.movie_name.replace('\t', ''), movie.movie_channel.replace('\t', ''), movie.movie_start+"-"+movie.movie_end, movie.movie_rating])
        print tabulate(data_movies2, headers=headers)"""

'''
        print("\nWant to save as pdf? Y/N")
        choice = raw_input().lower()
        if choice == 'y':
            pdf_save(data_movies2, headers)
            print('Saved!')
'''
if __name__ == '__main__':
    main()
