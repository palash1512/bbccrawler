
import time
import sys
from selenium import webdriver
import pymongo

# import BBC class from helper file
from helper import BBC

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('C:\\Users\\Nikunj\\Desktop\\Algotrading\\numdic\\chromedriver.exe', options=chrome_options)
wd.set_window_size(1280, 800)
wd.get('https://bbc.com')

# Find all the article links
links = wd.find_elements_by_class_name('media__link')

linkhref = []
for ln in links:
    linkhref.append(ln.get_attribute('href'))

# connet with mongo server
client = pymongo.MongoClient(
    "mongodb+srv://numadic:palashshah@bbc.u2vxe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# define Database
db = client['bbcdatabase']
# define collection
collection = db['bbcarticles']

# iterate over all the links
for link in linkhref:
    print(link)
    try:
        if 'news' in link:
            wd.get(link)

            # Crawler for Live news articles
            if 'Live Reporting' in wd.page_source:
                # Call BBC class for crawling link by giving header, editor, article body class name
                information = BBC(link, "lx-stream-post__header-text",
                                  "lx-commentary__meta-reporter", 'lx-stream-post-body')

                for no in range(len(information.header)):
                    document = {
                        'heading': information.header[no].text,
                        'article': information.articleBody[no].text,
                        'editor': information.editor,
                        'type': 'news',
                        'url': link
                    }
                    collection.insert_one(document)
                    print('1')
            # Crawl for normal news acticles
            else:
                information = BBC(link, 'ssrcss-1pl2zfy-StyledHeading',
                                  'ssrcss-1pjc44v-Contributor', 'e1xue1i84')

                wholearticle = " ".join(
                    [ar.text for ar in information.articleBody])

                document = {
                    'heading': information.header[0].text,
                    'article': wholearticle,
                    'editor': information.editor,
                    'type': 'news',
                    'url': link
                }
                collection.insert_one(document)
                print('news 2')

        # Crawl for other articles
        elif 'article' in link:
            information = BBC(link, 'article-headline__text',
                              'article__author-unit', 'article__body-content')

            document = {
                'heading': information.header[0].text,
                'article': information.articleBody[0].text,
                'editor': information.editor,
                'type': 'article',
                'url': link
            }
            collection.insert_one(document)

    except Exception as e:
        print(link)
        print(e)
