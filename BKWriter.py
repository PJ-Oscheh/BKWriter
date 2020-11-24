#BKWriter takes player usernames and UUIDs from EssentialsX and inserts them into ChestShop's users.db file.
#Use this script to enable ChestShops for Bedrock users.
#This code can theoretically be adapted for more than one use case (hence the generic name)

import sqlite3
import os
import ftplib
import pathlib
Path = pathlib.Path
version="1.0-20201124"

#==========CONFIGURATION==========

prefix = '*' #What prefix does Floodgates use to denote a Bedrock player?
chestshopdir = '/home/you/server/plugins/ChestShop' #Chestshop directory, excluding any files
essentialsxdir = '/home/you/server/plugins/Essentials' #EssentialsX directory, excluding any files

enable_ftp = False #Whether to enable FTP. For servers hosted by a company, you'll probably need to use this.
ftp_address = 'my.server.com' #FTP Address Here.
ftp_username = 'username' #FTP login
ftp_password = 'password' #FTP password

#If you're using FTP, make sure your chestshopdir and essentialsxdir are set to your LOCAL working directory!
#BKWriter will mirror your folder setup in this folder.

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

def useftp(option,fileName,i=0):
    fileName = Path(fileName)
    if option=='DOWNLOAD':
        print(f'Downloading {fileName}...')
        with ftplib.FTP(ftp_address,ftp_username,ftp_password) as ftp, open(fileName,'wb') as file:
            ftp.retrbinary(f"RETR {file.name}",file.write)
    elif option=='UPLOAD':
        print(f'Uploading {fileName}...')
        with ftplib.FTP(ftp_address,ftp_username,ftp_password) as ftp, open(fileName,'rb') as file:
            ftp.storbinary(f"STOR {file.name}",file)
    elif option =='COUNT':
        with ftplib.FTP(ftp_address,ftp_username,ftp_password) as ftp:
            return len(ftp.nlst(str(fileName)))
    elif option =='GET_FILE_NAME':
        with ftplib.FTP(ftp_address,ftp_username,ftp_password) as ftp:
            return ftp.nlst(str(fileName))[i]

def chestShop():
    if enable_ftp==True:
        if os.path.isdir(chestshopdir) ==False:
            print(f"ERROR: {chestshopdir} doesn't exist!\nPlease be sure to create all subfolders as well (as this function has not yet been implemented).")
            exit()
        if os.path.isdir(essentialsxdir) ==False:
            print(f"ERROR: {essentialsxdir} doesn't exist!\nPlease be sure to create all subfolders as well (as this function has not yet been implemented).")
            exit()
        if os.path.isdir(f'{essentialsxdir}/userdata') ==False:
            print(f"ERROR: {essentialsxdir}/userdata doesn't exist!\nPlease be sure to create all subfolders as well (as this function has not yet been implemented).")
            exit()
        useftp('DOWNLOAD','plugins/ChestShop/users.db')
        userFiles = useftp('COUNT','plugins/Essentials/userdata')
        for i in range(0,userFiles):
            essentials_uuid = useftp('GET_FILE_NAME','plugins/Essentials/userdata',i)
            useftp('DOWNLOAD',f'plugins/Essentials/userdata/{essentials_uuid}')
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

#Files to reupload to FTP Server
if enable_ftp==True:
    useftp('UPLOAD',Path('plugins/ChestShop/users.db'))