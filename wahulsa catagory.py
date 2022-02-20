#final_get_catagory
import requests
import math
import re
from bs4 import BeautifulSoup
import mysql.connector
# import csv
import json
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
def mail_send(s):
    fromaddr = "anandn@fcsus.com"
    toaddr = "nishadaman4438@gmail.com"
    msg = MIMEMultipart()
    # storing the senders email address  
    msg['From'] = fromaddr
    # storing the receivers email address 
    msg['To'] = toaddr
    # storing the subject 
    msg['Subject'] = "Differences between vnp & stock(qty) "
    # string to store the body of the mail
    body = s
    msg.attach(MIMEText(body, 'plain'))
    # open the file to be sent 
    s = smtplib.SMTP('smtp.office365.com', 587)
    s.starttls()  
    # Authentication(password)
    s.login(fromaddr, 'password')
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

def anand():
    mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
    )
    mycursor = mydb.cursor()
    mycursor.execute("""CREATE TABLE if not exists `wahlusa_categories` (
    `id` int NOT NULL AUTO_INCREMENT,
    `category` varchar(250) NOT NULL,
    `sub_category` varchar(250) NOT NULL,
    `sub_sub_category` varchar(250) NOT NULL,
    `stock` varchar(255) DEFAULT NULL,
    `product_url` varchar(250) NOT NULL,
    `processed` int NOT NULL DEFAULT '0',
    KEY `id` (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1""")

    link = requests.get("https://wahlusa.com/")
    html = link.content
    soup = BeautifulSoup(html,"lxml")
    x = soup.find_all('a',class_="pagebuilder-button-link")
    for i in x:
        link = (i.get("href"))
        # print(link)
        data = requests.get(link)
        html = data.content
        soup = BeautifulSoup(html,"lxml")
        # print(soup)
        x = soup.find_all('li',class_="item -is-collapsible -is-by-click -filter-parent")
        for i in x:
            n = i.find_all("a")
            for k in n:
                # print(k)
                if k.get("href") :
                    if "all-product" not in k:
                        stock = k.find('span', class_="count")
                        stock = stock.text.split()[0]
                        if stock == "0":
                            stock = "0"
                        else:
                            stock = "1"
                        links = k.get("href")
                        if "all-product" not in k.get("href"):
                            sub_catgary = links.split("/")
                            catgory = sub_catgary[3]
                            # print(links)
                            # print(stock)
                            if len(sub_catgary)>4:
                                sub_catgary = sub_catgary[4]
                            else:
                                sub_catgary = catgory
                            name = k.get("aria-label")
                            mycursor = mydb.cursor()
                            mycursor.execute("select id from `wahlusa_categories` where `product_url`=%s ",(links,))
                            result = mycursor.fetchall()
                            if result==[]:
                                mycursor = mydb.cursor()
                                val = list(zip((catgory,),(sub_catgary,),(name,),(stock,),(links,)))
                                sql = "insert into `wahlusa_categories`(`category`,`sub_category`,`sub_sub_category`,`stock`,`product_url`) values (%s,%s,%s,%s,%s)" 
        #                         print(sql)
                                mycursor.executemany(sql,val) 
                                mydb.commit()
def main():
    try:
        anand()
        s = "wahlusa cat is succesfully"
        mail_send(s)
    except:
        s = "wahlusa cat is unsuccesfully"
if __name__ == "__main__":
    main()
    
        
