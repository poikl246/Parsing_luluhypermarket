import random
import time
from time import sleep
import requests
from bs4 import BeautifulSoup
import json
import csv
import os

headers = {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/56.0.3051.52', 'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1'}

file_list = [['Name', 'Old price', 'Prise', 'Discount', 'Availability of tax', 'In stock']]
# file_list.append([name, old_price, price, discount, availability_of_tax, in_stock])


def request_no_error(url, retry=5):

    try:
        response = requests.get(url=url, headers=headers)
        print(f"[+] {url} {response.status_code}")
    except Exception as ex:
        time.sleep(3)
        if retry:
            print(f"[INFO] retry={retry} => {url}")
            return test_request(url, retry=(retry - 1))
        else:
            raise
    else:
        return response


for i in range(1815315, 1815315 + 50):

    url = f'https://www.luluhypermarket.com/en-ae/lulu-sunflower-oil-2-x-1-5litre/p/{i}'


    req = request_no_error(url=url, retry=1)

    src = req.text
    # print(src)

    with open("index.html", "w", encoding='utf-8') as file:
        file.write(src)

    # print(src)

    with open("index.html", encoding='utf-8') as file:
        src = file.read()

    # print(src)
    soup = BeautifulSoup(src, 'html.parser')

    try:
        name = soup.find(class_="product-details-page-main").find(class_="product-description").find(class_="product-name").find_next().text.strip()
    except:
        name = '---'


    try:
        old_price = soup.find(class_="product-details-page-main").find(class_="product-description").find(class_='price-tag detail').find(class_="off").text.strip()
    except:
        old_price = '---'


    try:
        price = soup.find(class_="product-details-page-main").find(class_="product-description").find(class_='price-tag detail').find(class_="item price").text.strip()
    except:
        price = '---'

    try:
        discount = soup.find(class_="product-details-page-main").find(class_="product-description").find(class_='price-tag detail').find(class_="item off-percent").text.strip()
    except:
        discount = '---'

    try:
        availability_of_tax = soup.find(class_="product-details-page-main").find(class_="product-description").find(class_='price-tag detail').find(class_="tax-instituion").text.strip()
    except:
        availability_of_tax = '---'

    try:
        in_stock = soup.find(class_="product-details-page-main").find(class_="stock").find(class_='in-stock').text.strip()
    except:
        in_stock = '---'



    print(name, '###', old_price, '###', price, '###', discount, '###', availability_of_tax, '###', in_stock)

    os.remove('index.html')

    if (name != '---') and (price != '---'):
        file_list.append([name, old_price, price, discount, availability_of_tax, in_stock])


print(file_list)


with open('exit_data.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerows(file_list)