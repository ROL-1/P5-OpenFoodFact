""" class to filter(really?) api informations and transmit it to the database."""
"""pip install mysql-connector-python"""


    #products = cursor.fetchall()

    #for product in products :
        #...

    #fetchone, fetchall, fetchmany #To Clean

# except MC.Error as err :
    # if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    #     print("Something is wrong with your user name or password")
    # elif err.errno == errorcode.ER_BAD_DB_ERROR:
    #     print("Database does not exist")
    # else:
    #     print(err)
    

import json
import mysql.connector as MC

with open("scraped_file.json", "r") as read_file:
    data = json.load(read_file)
    print(data['products'][0]['code'])

connection = MC.connect(host = 'localhost', database ='DBOFF1', user = 'root', password = 'mdp123')
cursor = connection.cursor()


add_brand = ("INSERT INTO brands (brands_id,brands_name) VALUES (%s,%s)") #requette pour ajouter une marque      
data_brand = (999,data['products'][0]['brands']) #marque test
# infos = (cursor.lastrowid, 'nutella','orangina') #cursor.lastrowid récupère le dernier id 

# request = 'SELECT * FROM DBOFF1' 

# insérer nouveau produit
cursor.execute(add_brand,data_brand)

# Make sure data is committed to the database
connection.commit() #Enregistre l'information

cursor.close()
connection.close()
