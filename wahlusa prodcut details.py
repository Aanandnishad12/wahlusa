
import requests
import math
import re
from bs4 import BeautifulSoup
import requests
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mysql.connector


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
    filename = "File_name_with_extension"
    attachment = open('./wahlusa_vnp.csv', "rb")
    
    parter1 = MIMEBase('application', 'octet-stream')
    parter1.set_payload((attachment).read())
    encoders.encode_base64(parter1)
    parter1.add_header('Content-Disposition', 'attachment', filename='wahlusa_vnp.csv')
    msg.attach(parter1)
    
    parter2 = MIMEBase('application', "octet-stream")
    parter2.set_payload(open('./wahlusa_stock.csv', "rb").read())
    encoders.encode_base64(parter2)
    parter2.add_header('Content-Disposition', 'attachment', filename='wahlusa_stock.csv')  
    msg.attach(parter2)

    parter3 = MIMEBase('application', "octet-stream")
    parter3.set_payload(open('./wahlusa_new_prod.csv', "rb").read())
    encoders.encode_base64(parter3)
    parter3.add_header('Content-Disposition', 'attachment', filename='wahlusa_new_prod.csv.csv')  
    msg.attach(parter3)
    
    s = smtplib.SMTP('smtp.office365.com', 587)
    s.starttls()  
    # Authentication(password)
    s.login(fromaddr, 'password')
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
new_prod = []
def anand():
 
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Anishad@123",
    database="experiment"
    )
    mycursor = mydb.cursor()
    mycursor.execute('''CREATE TABLE if not exists`wahlusa_op` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `Product_Title` varchar(900) DEFAULT NULL,
    `sku` varchar(600) DEFAULT NULL,
    `parent_sku` varchar(600) DEFAULT NULL,
    `primary_sku` int(1) DEFAULT NULL,
    `UPC` varchar(750) DEFAULT NULL,
    `EAN` varchar(36) DEFAULT NULL,
    `LMP_SKU` varchar(600) DEFAULT NULL,
    `mfg_id` varchar(90) DEFAULT NULL,
    `FF_Latency` varchar(30) DEFAULT NULL,
    `Amazon_ASIN` varchar(30) DEFAULT NULL,
    `is_change` char(1) DEFAULT NULL,
    `notions_unit_of_sale` int(3) DEFAULT NULL,
    `previous_vnp` decimal(7,2) DEFAULT NULL,
    `fcsus_unit_of_sale` int(3) DEFAULT NULL,
    `vnp` decimal(7,2) DEFAULT '0.00',
    `inward_freight` decimal(9,0) DEFAULT NULL,
    `description` text,
    `specification` text,
    `whats_in_box` varchar(1500) DEFAULT NULL,
    `details` varchar(1500) DEFAULT NULL,
    `price_update_override` int(1) DEFAULT NULL,
    `wgt_update_override` int(1) DEFAULT NULL,
    `Minimum_Advertised_Price` decimal(9,0) DEFAULT NULL,
    `frt_collect` varchar(3) DEFAULT NULL,
    `image1` varchar(1500) DEFAULT NULL,
    `image2` varchar(1500) DEFAULT NULL,
    `image3` varchar(1500) DEFAULT NULL,
    `image4` varchar(1500) DEFAULT NULL,
    `image5` varchar(1500) DEFAULT NULL,
    `previous_qty_avb` int(1) DEFAULT NULL,
    `qty_avb` int(1) DEFAULT NULL,
    `stock` int(1) DEFAULT NULL,
    `category` text,
    `sub_category` text,
    `url` text,
    `discontinued` int(1) DEFAULT NULL,
    `last_updated` varchar(765) DEFAULT NULL,
    `doba_categories` varchar(255) DEFAULT NULL,
    `doba_allowed` int(1) NOT NULL DEFAULT '1',
    KEY `id` (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8''')
    # mycursor.execute("ALTER TABLE ananddb.`wahlusa_op` CONVERT TO CHARACTER SET utf8")
    mycursor = mydb.cursor()
    Query = ("select * from  `wahlusa_categories` where `processed` = '0'")
    mycursor.execute(Query)
    result = mycursor.fetchall()
    if result != []:
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE `wahlusa_op`  SET previous_vnp = vnp")
        mycursor = mydb.cursor()
        mycursor.execute('UPDATE `wahlusa_op`  SET previous_qty_avb = qty_avb')
    # mycursor.execute("select * from `wahlusa_categories` where `processed` = 0" )
    # result = mycursor.fetchall()
    # print(re)
    for link in result:
     
        print(link)
        url = link[5]
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE `wahlusa_categories` SET `processed` = '1' WHERE product_url = %s", (url,))
        # print(link[1])
        catgory = link[1]
        sub_catgary = link[2]
        sub_sub_category = link[3]
        response = requests.get(link[5])
        soup = BeautifulSoup(response.content,"lxml")
        total_prod = soup.find_all('span',class_="toolbar-number")
        n = 0
        for i in total_prod:
            n+=1
            no = i.text
        # print(no)
        if n==3:
            page = math.ceil(int(total_prod[-1].text)/int(total_prod[-2].text))
        else:
            page = 1
        for j in range(1,page+1):
            response = requests.get(link[5]+"?p="+f'{j}')
            soup = BeautifulSoup(response.content,"lxml")
            prod_link = soup.find_all('a',class_="product-item-link")
            for k in prod_link:
                
                if k.text.strip():
                    name = k.text.strip().replace("'","")
    #                 print(name)
                if k.get("href"):
                    link1= k.get("href")
    #                 print(link1)
                    upccode = ''
                    response = requests.get(link1)
                    soup = BeautifulSoup(response.content,"lxml")
                    price = soup.find('span',class_="price")
                    if price:
                        price = price.text.replace("$","")
        #                 print(price)
                    sku = soup.find('div',class_="value")
                    if sku:
                        sku = sku.text
        #                 print(sku)
                    details = soup.find('div',class_="product attribute description")
                    if details:
                        details = details.text.replace('"',"-Inches").replace("'",'')
        #                 print(details)
                    description = soup.find('div',class_="product attribute overview")
                    if description:
                        description = description.text.replace('"',"-Inches").replace("'",'')
        #                 print(description)
                    spec = soup.find_all('th',class_="col label")
                    spec_ = soup.find_all('td',class_="col data")
                    if spec or spec_:
                        s = ","
                        for i in zip(spec,spec_):
                            s = (i[0].text+"--"+i[1].text)+s
                        specification = s.replace("'",'')
        #                 print(specification)
                    whats_in_box = soup.find('dl',class_="col-lg-3 col-sm-6 col-xs-12")
                    if whats_in_box:
                        whats_in_box = whats_in_box.text.replace('\n',",").replace('#',"").replace('"',"-Inches").replace("'",'')
                    image = soup.find("img",class_="gallery-placeholder__image")
                    if image:
                        image = image.get("src")
        #                 print(image)
                    stock = soup.find('div',class_="product-info-price")
                    if stock:
                        stock = re.search(r'<span>(.*?)</span>',str(stock)).group(1)
                        if len(stock)==12:
                            stock = str(0)
                        else:
                            stock = str(1)
                    if price=='0' or name=='':
                        discontinued=1
                    else:
                        discontinued=0
        #             print(stock)
                    mycursor = mydb.cursor()
                    mycursor.execute("select id from `wahlusa_op` where `url`=%s ",(link1,))
                    result = mycursor.fetchall()
                    if result==[]:
                   
                        new_prod.append(sku)
                        val=list(zip((name,),(sku,),(sku,),(upccode,),(price,),(description,),(specification,),(whats_in_box,),(details,),(image,),(stock,),(catgory,),(sub_catgary,),(link1,),(discontinued,)))
                        sql = """insert into `wahlusa_op`(`Product_Title`, `sku`, `parent_sku`,`UPC`,`vnp`,`description`,`specification`,`whats_in_box`,`details`,`image1`,`stock`,`category`,`sub_category`,`url`,`discontinued`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" 
                        mycursor.executemany(sql,val) 
                        mydb.commit()
                    else:
                      
                        mycursor = mydb.cursor()
                        mycursor.execute("UPDATE `wahlusa_op` SET `vnp`= %s,`stock`=%s WHERE `sku` = %s ", (price,stock,sku,)) 
                        mydb.commit()
    mycursor = mydb.cursor()
    mycursor.execute("UPDATE `wahlusa_op`  SET qty_avb = stock") 
    mydb.commit()

    mycursor = mydb.cursor()        
    mycursor.execute("select sku,vnp,previous_vnp,previous_qty_avb,qty_avb from `wahlusa_op`")
    result = mycursor.fetchall()
    with open('wahlusa_vnp.csv', 'w',  newline='') as outcsv:
            writer = csv.writer(outcsv)
            writer = csv.DictWriter(outcsv, fieldnames = ["sku", "vnp", "previous_vnp"])
            writer.writeheader()
            
    with open('wahlusa_stock.csv', 'w',  newline='') as stcsv:
            writers = csv.writer(stcsv)
            writers = csv.DictWriter(stcsv, fieldnames = ["sku", "previous quantity", "quantity available"])
            writers.writeheader()
    with open('wahlusa_new_prod.csv', 'w',  newline='') as skucsv:
            writers = csv.writer(skucsv)
            writers = csv.DictWriter(skucsv, fieldnames = ["new_prod"])
            writers.writeheader()

    for x in result:
        sku=x[0]
        vnp= x[1]
        pvnp= x[2]
        pqty=x[3]
        qty=x[4]
        if vnp!=pvnp:
            print(vnp)
            with open('wahlusa_vnp.csv', 'a', newline='') as vnpcsv:
                writer = csv.writer(vnpcsv)
                writer = csv.DictWriter(vnpcsv, fieldnames =[sku,vnp,pvnp])
                writer.writeheader()
        if pqty != qty:
            with open('wahlusa_stock.csv', 'a', newline='') as stockcsv:
                writers = csv.writer(stockcsv)
                writers = csv.DictWriter(stockcsv, fieldnames =[sku,pqty,qty])
                writers.writeheader()
    for i in new_prod:
        with open('wahlusa_new_prod.csv', 'a', newline='') as vnpcsv:
            writer = csv.writer(vnpcsv)
            writer = csv.DictWriter(vnpcsv, fieldnames =[i])
            writer.writeheader()
def main():
    try:
        anand()
        s = "wahlusa op is sucsessful"
        mail_send(s)
    except:
        s = "wahlusa op is unsucsessful"
        mail_send(s)
if __name__ == "__main__":
    main()
