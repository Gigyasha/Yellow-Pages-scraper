#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options 
import time
from bs4 import BeautifulSoup
import pandas as pd
import csv
from random import randint
from selenium.webdriver.support.wait import WebDriverWait
 
url="https://www.indiacom.com/yellow-pages/hospitals/ahmedabad/?page=10"
link=url
chrome_options = Options()  
chrome_options.add_argument("--headless")  
driver =webdriver.Chrome(executable_path=r'C:\Users\DELL\.wdm\drivers\chromedriver\80.0.3987.106\win32\chromedriver.exe')
driver.get(url)
time.sleep(3)

bl=0
data_link=[]
while True:
    elem_list=driver.find_elements_by_class_name("b_listing")
    for e in elem_list:
        try:
            #print(e.text)
            
            name_tag=e.find_element_by_class_name("b_name_rating")
            #print(name_tag.text)
            nn=name_tag.find_element_by_class_name("b_name")
            a_tag=nn.find_element_by_tag_name("a").get_attribute("href")
            data_link.append(a_tag)
            print(a_tag)
        except Exception as e:
            print("NO A TAG",e)
            continue
    try:
        time.sleep(2)
        pagination=driver.find_element_by_xpath('//*[@id="divlisting"]/div[63]')
        #print(pagination.text)
        a_tags=pagination.find_elements_by_tag_name("a")
        next_pg=None
        for a in a_tags:
            if a.text=="Next":
                next_pg=a.get_attribute("href")
        
        if next_pg is not None:
            driver.get(next_pg)
            time.sleep(2)
        else:  
            break
    except Exception as e:
        print("NO NEXT",e)
        break
print(len(data_link))
place="mumbai"
state="maharashtra"
head=["name","phone","address","category","place","state"]
with open('ahembadad_hospital_yellow.csv', mode='a+',encoding="UTF-8",newline="") as file:
    writer1 = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer1.writerow(head)
    for li in data_link:
        try:
            driver.get(li)
            name=None
            address=None
            phone=None
            cat=None
            time.sleep(2)
            button=driver.find_element_by_id("btn_phone").click()
            time.sleep(2)
            try:
                block=driver.find_element_by_id('div_details')
                nn=block.find_element_by_class_name("div_bizname")
                name=nn.find_element_by_tag_name("h1").text

                detail_block=block.find_element_by_id("div_phoneadd")
                cat=detail_block.find_element_by_class_name("divcat").text
                det=detail_block.find_elements_by_class_name("lighttext")
                for l in det:
                    if "hone" in l.text:
                        phone=(l.find_element_by_tag_name("a").text).strip()
                        phone=phone.replace("Phone :"," ",1)

                add=detail_block.find_elements_by_class_name("mr10") 
                for k in add:
                    #print(k)
                    if "ddress" in k.text:
                        address=(k.text).strip()
                        address=address.replace("Address :"," ",1)
                bl=bl+1
                writer1.writerow([name,phone,address,cat,place,state])
                print("BLOCK--->>",bl," COMPLETED")
                print("NAME",name)
                print("PHONE",phone)
                print("ADDRESS",address)
                print("CATEGORY",cat)
            except Exception as e:
                print("detail issue",e)
                continue 
        except Exception as e:
            print("no button",e)
            continue
