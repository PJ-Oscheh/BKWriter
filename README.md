# BKWriter
A quick-n-dirty solution to make the Chestshop plugin work on Java servers for Bedrock players connected via Floodgates. Talk about a specific issue

This is a simple script that manually adds any Bedrock players to Chestshop's users.db file. I don't know Java, let alone how to make a proper plugin, so this is what I got. The script probably needs to be run locally and connect via FTP to modify the file.

I designed this for my own server, Burg Kurg (hence the "BK"), but it may be used on any server!

Requires Chestshop*

Requires EssentialsX**

\* The code can theoretically be adapted for any other plugin. If the target plugin uses a setup identical to Chestshop's, you can just change the Chestshop's directory in the Configuration

** EssentialsX is used to pull player's usernames and UUIDs

# How to Configure:
To configure this script, you'll need to open it directly. All the options are located near the top of the script under `CONFIGURATION`. Take a look:

```
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
```
Just slap your option in there and you're good to go!

Still WIP I guess.
