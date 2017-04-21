#date : 14 January 2017
# -*- coding: utf-8 -*-
import requests
import urllib
import os
import xml.etree.cElementTree as ET
from BeautifulSoup import BeautifulSoup

root = "NewDatabase"
last = "Database"
url =  "http://www.markafoni.com/"
soup = BeautifulSoup(requests.get(url).content)
categories = soup.findAll("li",{"class":"category"})#menüdeki kategoriler
if (os.path.exists(root)==False):
    os.mkdir(root)
categoryHeaders = [[13],[11]]#kadın -> tesettür ok 2, elbise ok 3, mont ok 4, gömlek ok 13, tulum ok 15, triko ok 18
for i in [1]: #kadın ok 0, erkek          #erkek -> triko ok 8, mont ok 9, gömlek ok 10, pantolon
    subcategories = categories[i].find("ul",{"class":"headermenu-categories"}).findAll("a")#alt kategoriler
    sex = categories[i].find("a",{"class":" "}).text

    check = root + os.sep + sex#Cinsiyet listeleri
    if(os.path.exists(check)==False):
        os.mkdir(check)

    for j in categoryHeaders[i]:
        tempcategory = subcategories[j]#giyim kategorileri
        check = root + os.sep + sex + os.sep + tempcategory.text + os.sep
        if(os.path.exists(check) == False):
            os.mkdir(check)

        items = ET.Element("items")

        templink = tempcategory.get("href")
        tempsoup = BeautifulSoup(requests.get(templink).content)
        title = str(tempsoup.find("section",{"class":"title-content"}).find("sup"))
        dowloaded = 0
        itemCount = 0
        for s in title.split():
            if s.replace(".","").isdigit():
                itemCount = int(s.replace(".", ""))

        while(dowloaded<itemCount):
            templink = tempcategory.get("href")+"?sz=12&start="+str(dowloaded)
            itemSoup = BeautifulSoup(requests.get(templink).content).findAll("div",{"class":"item-container"})
            for it in itemSoup:
                print(str(dowloaded))
                imagelink = it.find("div",{"class":"image-container"}).find("img").get("data-original")
                price = it.find("div",{"class":"new-price"}).text
                iteminfo = it.find("a",{"class":"ee-product"})
                itemlink = url + iteminfo.get("href")
                brand = iteminfo.find("div").text

                item = ET.SubElement(items, "item")
                ET.SubElement(item,"imagelink").text = imagelink
                ET.SubElement(item, "price").text = price
                ET.SubElement(item, "itemlink").text = itemlink
                ET.SubElement(item, "brand").text = brand
                if (os.path.exists(check + str(dowloaded))):
                    dowloaded += 1
                    continue
                urllib.urlretrieve(imagelink,check+str(dowloaded))
                dowloaded += 1
        tree = ET.ElementTree(items)
        tree.write(check+"data.xml")
os.rename(root,last)
