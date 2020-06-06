from flask import Flask, jsonify, make_response, request, abort
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

BASE_URL = 'https://www.flipkart.com';

if __name__ == '__main__':
    app.run()
    
@app.route('/products', methods=['GET'])
def getProductsDetails():
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
            name = name + span.text
        product['name'] = name
        product['price'] = prod_soup.find('div',{'class':'_1vC4OE _3qQ9m1'}).text
        
        rev_rat_tag = prod_soup.find('span',{'class':'_38sUEc'})
        
        if rev_rat_tag is not None:
            product['noOfRatingsAndReviews'] = rev_rat_tag.text
        else:
            if 'Be the first to Review this product' in prod_soup.find('span',{'class':'_1IcGRZ'}).text:
                product['noOfRatingsAndReviews'] = '0 ratings & 0 reviews';
        
        product['link'] = link
        
        products.append(product)
        
    #return make_response(jsonify({'Products':products, 'Count':len(products), 'Urls': urls}), 200)
    return make_response(jsonify({'Products':products, 'count':len(products)}), 200)

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