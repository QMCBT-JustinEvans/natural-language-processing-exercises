###################
##### IMPORTS #####
###################

import pandas as pd
from bs4 import BeautifulSoup
import requests
from requests import get

def get_blog_articles(url):
    """
    Description:
    This function scrapes Codeup Blog site (https://codeup.com/blog/) for article urls 
    then scrapes the title and content from those urls and returns them in a dictionary.

    Required Imports:
    import pandas as pd
    from bs4 import BeautifulSoup
    import requests
    from requests import get
    
    Arguments:
    url = The root page that holds the blog articles to be scraped.
    
    Returns:
    articles - a dictionary containing:
                'title': 'the title of the article',
                'content': 'the full text content of the article'
    """
    
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    links = [link['href'] for link in soup.select('.more-link')]

    articles = []

    for url in links:

        url_response = get(url, headers=headers)
        soup = BeautifulSoup(url_response.text)

        title = soup.find('h1', class_='entry-title').text
        content = soup.find('div', class_='entry-content').text.strip()

        article_dict = {
            'title': title,
            'content': content
        }

        articles.append(article_dict)
    
    return articles
    
    #articles_df = pd.DataFrame(articles)
    #articles_df.to_csv('articles.csv', index=False)
    #return articles_df

def get_news_articles(url, category_list):
    """
    Description:
    This function scrapes the news site (https://inshorts.com/en/read) for article title and content 
    given the category as an argument and returns them in a dictionary.
    
    Required Imports:
    import pandas as pd
    from bs4 import BeautifulSoup
    import requests
    from requests import get
    
    Arguments:
              url = The root page that hplds the blog articles to be scraped.
    category_list = A LIST of 'category' of news articles to scrape (will accept single item list).
    
    Returns:
    articles - a dictionary containing:
                'category' the type of the news article
                'title': 'the title of the article'
                'content': 'the full text content of the article'
    """
    categories = category_list
    #categories = ['business', 'sports', 'technology', 'entertainment']
    #categories = [li.text.lower() for li in soup.select('li')][1:]
    #categories[0] = 'national'

    articles = []

    for category in categories:

        url = 'https://inshorts.com/en/read' + '/' + category
        response = get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        categories = [li.text.lower() for li in soup.select('li')][1:]
        titles = [span.text for span in soup.find_all('span', itemprop='headline')]
        contents = [div.text for div in soup.find_all('div', itemprop='articleBody')]

        for i in range(len(titles)):

            article_dict = {
                'title': titles[i],
                'content': contents[i],
                'category': category,
            }

            articles.append(article_dict)
            
    return articles
    
    #articles_df = pd.DataFrame(articles)
    #articles_df.to_csv('articles.csv', index=False)
    #return articles_df