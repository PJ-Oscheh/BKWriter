#BKWriter takes player usernames and UUIDs from EssentialsX and inserts them into ChestShop's users.db file.
#Use this script to enable ChestShops for Bedrock users.
#This code can theoretically be adapted for more than one use case (hence the generic name)

import sqlite3
import os
version="1.0-20201124"

#==========CONFIGURATION==========

prefix = '*' #What prefix does Floodgates use to denote a Bedrock player?
chestshopdir = '/home/pj/burgKurgTest/plugins/ChestShop' #Chestshop directory, excluding any files
essentialsxdir = '/home/pj/burgKurgTest/plugins/Essentials' #EssentialsX directory, excluding any files

#=================================

#Functions for reading the database
def importdb(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT * FROM accounts')
    data = c.fetchall()
    return data
def exportdb(db,newData):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("INSERT into accounts VALUES(?,?,?,?)",newData)
    conn.commit()

def chestShop():
    usersdb = importdb(f'{chestshopdir}/users.db') #Open users.db from ChestShop as a list
    eUserData = os.listdir(f'{essentialsxdir}/userdata') #Directory with EssentialsX userdata files

    userDictionary = {} #Store names to be added to ChestShop user.db

    increment = 0 #Increment for userDictionary index

    #Detect Bedrock users and save them to userDictionary
    for i in range (0,len(eUserData)):
        if os.path.isfile(f'{essentialsxdir}/userdata/{eUserData[i]}'):
            with open(f'{essentialsxdir}/userdata/{eUserData[i]}','r') as f:
                for line in f:
                    line = line.rstrip()
                    if "lastAccountName" in line and prefix in line:
                        line = line[18:-1]
                        print(f"Name: {line}")
                        username = line
                        print(f'UUID: {eUserData[i][:-4]}')
                        uuid = eUserData[i][:-4]
                        userDictionary[increment] = [username,username,uuid,0]
                        increment +=1
                        break

    #Write users from userDictionary to users.db, given they don't already exist in the database.
    for i in range(0,len(userDictionary)):
        if str(userDictionary[i][0]) not in str(usersdb): #Convert these values to strings to make them easier to compare.
            print(f"Writing {userDictionary[i][0]}'s data...")
            exportdb(f'{chestshopdir}/users.db',userDictionary[i])
        else:
            print(f"Skipping {userDictionary[i][0]}'s data as it already exists.")

print(f"BKWriter version {version}\n")

#Add functions here, if you desire more data to be written
chestShop()