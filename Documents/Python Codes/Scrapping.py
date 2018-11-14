'''
Scrapping the imdb website to get the list of movie title
''' 
import urllib.request
import csv 
from bs4 import BeautifulSoup
import atexit
from multiprocessing import Pool
imdbNextPageUrlPrefix="https://www.imdb.com/search/title?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=b9121fa8-b7bb-4a3e-8887-aab822e0b5a7&pf_rd_r=012B67T39C2JQSZ4BB33&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=moviemeter&genres=action&genres=Action&explore=title_type,genres&"
imdbNextPageUrlPostFix="&ref_=adv_nxt"
MovieCollectionByName=[]
NumberofPages=201
NUM_PROCESSES = 7


#checking the given values is None or Not
def checkForNone(item):

    if(item is not None):
        return(True)
    return(False)

#Wrttting the  list of mvoies to CSV file
def writingResultsToCsv():

    with open('movielist4.csv', 'w', newline='') as file:
        writer = csv.writer(file) 
        for movie in MovieCollectionByName:
            writer.writerow(movie)

#Getting the list of divs from the Html page which has movie names
def getDivsHasMovieName(soup):

    return(soup.find_all("div", {"class":"lister-item-image float-left"}))

#Getting the URL which has list of the some movies 
def getUrl(page):

    return(imdbNextPageUrlPrefix+"page="+str(page)+imdbNextPageUrlPostFix)

#defining exit handler
def exit_handler():
    print("Programme is exiting")
    writingResultsToCsv()
    
atexit.register(exit_handler)

# get list of movies for given url which uses request package of urlib library
def getThelistOfMovies(imdbURL):
    Movies=[]
    try:
        with urllib.request.urlopen(imdbURL) as url:

            #reading the webpage using requests module
            page= url.read()
            soup = BeautifulSoup(page, 'html.parser')

            # Collecting all the divs which have movies name
            listofDivs = getDivsHasMovieName(soup)

            if(checkForNone(listofDivs)): # check wether the list of divs is empty or not
                for div in listofDivs:
                    Movies.append([div.find("img")["alt"]])
            return(Movies)

    except(RuntimeError, TypeError, NameError):
        print("Some error has occured")
# execute URL in parallel to speedup the execution 
def multiThreadExecutionOfUrls():

    Urls=[getUrl(page) for page in range(1,NumberofPages)]

    #Multithread
    ChunkResults = Pool(NUM_PROCESSES).map(getThelistOfMovies,Urls)
    for chunk in ChunkResults:
        for movie in chunk:
            MovieCollectionByName.append(movie)
    print(MovieCollectionByName)
if __name__ == "__main__":
    multiThreadExecutionOfUrls()
