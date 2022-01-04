import json

from bs4 import BeautifulSoup
import requests

url = "https://www.jumia.com.eg/"
html = requests.get(url).text
HTML = BeautifulSoup(html , 'html.parser')

SuperCategories = HTML.find_all('a' , class_='itm')
SuperCategoriesList = []
for i in SuperCategories:
    Span = i.find('span')
    attrs = i.attrs
    if Span != None and 'href' in attrs.keys() :
        link = url[:-1] + i['href']
        SuperCategoriesList.append(
            {
                'Category' : Span.text ,
                'Link' : link
            }
        )

################## Get Products in One Page of Category
ListProductsALL = []
cnt = 0
for j in SuperCategoriesList:
    if cnt == 1 :
        break
    cnt+=1
    ListProductsCategory = []
    Cat = j['Link']
    html = requests.get(Cat).text
    BS = BeautifulSoup(html , 'html.parser')
    Products = BS.find_all('article' , class_='c-prd')
    ProductsList = []
    for i in Products :
        Product = {}
        ProductInfo = i.find('div' , class_='info')
        ProductName = ProductInfo.find('h3' , class_='name').text
        ProductPrice = ProductInfo.find('div' , class_='prc').text
        ProductLink  = i.find('a' , class_='core')
        link_attrs = ProductLink.attrs
        if 'href' in link_attrs.keys():
            Product['Link'] = Cat[:-1] + ProductLink['href']
        if ProductName != '' :
            Product['Name'] = ProductName
        if ProductPrice != '':
            Product['Price'] = ProductPrice
            ProductsList.append(Product)
    ListProductsCategory.append({'1' : ProductsList})
    page=2
    while True :
        print(page)
        ReqHTML = requests.get(f'{Cat}+?page={page}#catalog-listing')
        if ReqHTML.status_code != 200:
            break
        ReqHTML = ReqHTML.text
        BS = BeautifulSoup(ReqHTML, 'html.parser')
        Products = BS.find_all('article', class_='c-prd')
        if len(Products) == 0 or Products == None:
            break
        ProductsList = []
        for i in Products:
            Product = {}
            ProductInfo = i.find('div', class_='info')
            ProductName = ProductInfo.find('h3', class_='name').text
            ProductPrice = ProductInfo.find('div', class_='prc').text
            ProductLink = i.find('a', class_='core')
            link_attrs = ProductLink.attrs
            if 'href' in link_attrs.keys():
                Product['Link'] = Cat[:-1] + ProductLink['href']
                ProductPage = requests.get(Product['Link']).text
                ProductHTML = BeautifulSoup(ProductPage, 'html.parser')
                ProductInfo = {}
                ProductImageLink = ProductHTML.find('img', class_='-fw')
                ProductDetails = ProductHTML.find('div', class_='-mtm')
                DescriptionsList = []
                if ProductDetails.find('div', class_='-mhm'):
                    Descriptions = ProductDetails.find('div', class_='-mhm').find_all('p')
                    for i in Descriptions:
                        DescriptionsList.append(i.text.replace(u'\xa0', u' '))

                Specifications = ProductHTML.find_all('div', class_='-fh')
                ProductKeyFeatures = Specifications[0].find_all('li')
                ProductKeyFeaturesList = []
                for i in ProductKeyFeatures:
                    ProductKeyFeaturesList.append(i.text)

                ProductSpecifications = Specifications[1].find_all('li')
                ProductSpecificationsList = []
                for i in ProductSpecifications:
                    ProductSpecificationsList.append(i.text)
                FinalProductDetail = {
                    'KeyFeatures': ProductKeyFeaturesList,
                    'Specifications': ProductSpecificationsList,
                    'ProductImage': ProductImageLink['data-src'],
                    'Link': Product['Link'],
                    'Descriptions': DescriptionsList,
                    'Name': ProductName,
                    'Price': ProductPrice
                }
                print(FinalProductDetail)
                ProductsList.append(FinalProductDetail)
        ListProductsCategory.append({page: ProductsList})
        page+=1

    ListProductsALL.append({j['Category'] : ListProductsCategory })
print(ListProductsALL)
json_object = json.dumps(ListProductsALL, indent=4)

# Writing to sample.json
with open("sample.json", "w") as outfile:
    outfile.write(json_object)

# exit()
#
# ################## Details of Each Product ################################
# for j in ListProductsALL:
#     for k in j :
#         SingleProduct = k
#         ProductPage = requests.get(SingleProduct['Link']).text
#         ProductHTML = BeautifulSoup(ProductPage , 'html.parser')
#         ProductInfo = {}
#         ProductImageLink = ProductHTML.find('img' , class_='-fw')
#         ProductDetails = ProductHTML.find('div' , class_='-mtm')
#         DescriptionsList = []
#         if ProductDetails.find('div' , class_='-mhm'):
#             Descriptions = ProductDetails.find('div' , class_='-mhm').find_all('p')
#             for i in Descriptions:
#                 DescriptionsList.append(i.text.replace(u'\xa0', u' '))
#
#         Specifications =ProductHTML.find_all('div' , class_='-fh')
#         ProductKeyFeatures = Specifications[0].find_all('li')
#         ProductKeyFeaturesList = []
#         for i in ProductKeyFeatures:
#             ProductKeyFeaturesList.append(i.text)
#
#         ProductSpecifications = Specifications[1].find_all('li')
#         ProductSpecificationsList = []
#         for i in ProductSpecifications:
#             ProductSpecificationsList.append(i.text)
#         FinalProductDetail = {
#             'KeyFeatures' : ProductKeyFeaturesList ,
#             'Specifications' : ProductSpecificationsList,
#             'ProductImage' : ProductImageLink['data-src'] ,
#             'Link' : SingleProduct['Link'] ,
#             'Descriptions' : DescriptionsList ,
#             'Name' : SingleProduct['Name'] ,
#             'Price' : SingleProduct['Price']
#             }
#         print(FinalProductDetail)






