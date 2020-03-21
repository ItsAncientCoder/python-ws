from flask import Flask, jsonify, make_response, request, abort
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

BASE_URL = 'https://www.flipkart.com';

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run()
    
@app.route('/urls', methods=['GET'])
def getProductUrls():
    keyword = request.args.get('q')
    response = makeHttpCallGetResponse(keyword)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = set()
    
    for a in soup.find_all('a',{'class':'_3dqZjq'}):
        urls.add(BASE_URL + a.get('href'))
    
    for a in soup.find_all('a',{'class':'_2cLu-l'}):
        urls.add(BASE_URL + a.get('href'))
        
    for a in soup.find_all('a',{'class':'_31qSD5'}):
        urls.add(BASE_URL + a.get('href'))
    
    urls = list(urls)
        
    # urls removing
    #t_urls = list()
    #for u in range(2):
        #t_urls.append(urls[u])
    #urls = t_urls
    
    products = list()
        
    for link in urls:
        product = dict()
        prod_soup = BeautifulSoup(requests.get(link).text,'html.parser')
    
        # name, price, review count & ratings count
        name_price_tag = prod_soup.find('h1',{'class':'_9E25nV'})
        name = ''
        for span in name_price_tag.find_all('span'):
            name = name + ' ' + span.text
        product['name'] = name
        product['price'] = prod_soup.find('div',{'class':'_1vC4OE _3qQ9m1'}).text
        
        product['noOfRatingsAndReviews'] = prod_soup.find('span',{'class':'_38sUEc'}).text
        
        products.append(product)
        
    #return make_response(jsonify({'Products':products, 'Count':len(products), 'Urls': urls}), 200)
    return make_response(jsonify({'Products':products, 'Count':len(products)}), 200)

@app.route('/products', methods=['GET'])
def getProducts():
    keyword = request.args.get('q')
    response = makeHttpCallGetResponse(keyword)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = set()
    
    for a in soup.find_all('a',{'class':'_3dqZjq'}):
        urls.add(a.get('href'))
    
    for a in soup.find_all('a',{'class':'_2cLu-l'}):
        urls.add(a.get('href'))
        
    for a in soup.find_all('a',{'class':'_31qSD5'}):
        urls.add(a.get('href'))
        
    print('no of product links found', len(urls))
    
    # extracting product details
    products = list()
    for link in urls:
        product = dict()
        prod_soup = BeautifulSoup(requests.get(link).text,'html.parser')
    
        # name, price, review count & ratings count
        name_price_tag = prod_soup.find('div',{'class':'_29OxBi'})
        name = ''
        for span in name_price_tag.find_all('span'):
            name = name + span.text
        product['name'] = name
        product['price'] = prod_soup.find('div',{'class':'_1vC4OE _3qQ9m1'}).text
        
        # TODO Improve
        noOfRatings = None
        noOfReviews = None
        try:
            rev_rat_tag = prod_soup.find('span',{'class':'_38sUEc'}).span.find_all('span')
            noOfRatings = rev_rat_tag[0].text
            noOfReviews = rev_rat_tag[2].text
        except Exception as e:
            print(e)
            noOfRatings = ''
            noOfReviews = ''
        product['no.of review'] = noOfRatings
        product['no.of ratings'] = noOfReviews
        
        # highlights
        try:
            highlights_tags = prod_soup.find('div',{'class':'_3WHvuP'}).find_all('li',{'class':'_2-riNZ'})
            highlights = [fea.text for fea in highlights_tags]
            product['highlights'] = highlights
        except Exception as e:
            print(e)
            product['highlights'] = list()
    
        # specifications
        specs_box_tag = prod_soup.find('div',{'class':'MocXoX'})
        specs = dict()
        if specs_box_tag is not None:
            specs_tag = specs_box_tag.find_all('div',{'class':'_2RngUh'})
            for spec_tag in specs_tag:
                td_tags = [tr.find_all('td') for tr in spec_tag.find_all('tr')]
                for td in td_tags:
                    if len(td)==2:
                        specs[td[0].text] = td[1].text
        else:
            specs = {}
        product['specifications'] = specs
    
        # reviews
        reviews = list()
        review_tags_parent = prod_soup.find_all('div',{'class':'_3nrCtb'})
        for rev_tag in review_tags_parent:
            try:
                review = dict()
                review['rating'] = rev_tag.find('div',{'class':'hGSR34 E_uFuv'}).text
                review['title'] = rev_tag.find('p',{'class':'_2xg6Ul'}).text
                review['message'] = rev_tag.find('div',{'class':'qwjRop'}).text
                review['customerName'] = rev_tag.find('p',{'class':'_3LYOAd _3sxSiS'}).text
                reviews.append(review)
            except Exception as e:
                print(e)
                pass
            
        product['reviews'] = reviews
        products.append(product)

    print(products)
    return make_response(jsonify({'products':products}), 200)

def makeHttpCallGetResponse(keyword):
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
        'Sec-Fetch-Dest': 'document',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    params = (
        ('q', keyword),
        ('otracker', 'search'),
        ('otracker1', 'search'),
        ('marketplace', 'FLIPKART'),
        ('as-show', 'off'),
        ('as', 'off'),
    )

    response = requests.get('https://www.flipkart.com/search', headers=headers, params=params)
    return response;