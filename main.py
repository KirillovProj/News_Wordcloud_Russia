import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
import nltk


# Collects headers of all news about Russia from past month in Google News (lang=en, region=US)
# Clears text from all numbers, prepositions, pronouns, particles etc, leaving only meaningful words
def get_words() -> list:
    wordlist = []
    pages = 0
    while True:
        r = requests.get('https://www.google.com/search?q=russia&tbm=nws&tbs=qdr:m&ceid=US:en&hl=en-US&gl=US', params={'start':pages}).text
        soup = BeautifulSoup(r, 'lxml')
        headers = soup.find_all('h3')
        if not headers:
            break
        for r in headers:
            formatted = r.find('div').text.replace('\n', '').replace('  ', '').replace('...', '').split()
            for word in formatted:
                if word.isalpha():
                    wordlist.append(word)
        pages += 10
    tagged = nltk.pos_tag(wordlist)
    result = [word[0] for word in tagged if word[1] not in [
        'CC', 'DT', 'EX', 'IN', 'PDT', 'PRP', 'PRP$', 'RP', 'WDT', 'WP', 'WP$', 'WRB', 'TO'
    ]]
    return result

# Uses map of Russia mask
def create_wordcloud():
    map_mask = np.array(Image.open('map.png'))
    stopwords = set(STOPWORDS)
    stopwords.update(['Russia', 'Russian', 'says', 'will'])
    wc = WordCloud(background_color='white', stopwords=stopwords, max_words=200, mask=map_mask).generate(' '.join(get_words()))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('Russian_News_Wordcloud.png', format='png')

if __name__ == '__main__':
    create_wordcloud()