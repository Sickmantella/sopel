"""
Sopel Database Plugin Loading Module

Copyright Liam 2021 All rights reserved.

This module provides the following:
 >  <Placeholder>

This module depends on:
 >  <Placeholder>
 
"""

from sopel import module #Allows access to bot stuff
import mariadb           #Allows access to the database of plugins
from sopel import tools  #Allows access to more bot stuff

class db:                #Defines the class db so you can do db.*()
    def connect(bot):    #Defines a connection to the bot
        try:             #Trys to connect to the database
            global conn  #Allows global access
            global cur
            conn = mariadb.connect( #Defines the connection username, password ect.
                user="Not_Here",
                password="N0T_H3R3!",
                host="127.0.0.1",
                port=3306,
                database="Not_Here"
            )
            cur = conn.cursor()    #Defines cur
            conn.autocommit = True #Allowa auto save
        except mariadb.Error as e: #Caches any errors connecting to the database
            bot.say(f"Error connecting to MariaDB Platform: {e}", "#tea-logs") #Puts the errors in the log channel of the bot

    def add_plugin(bot, nick, Plugin_Name): #Defines adding a plugin
        cur = conn.cursor() #Sets cur again
        try: #Tries to insert data into the database
            cur.execute("INSERT INTO Enabled_Plugins (Plugin_Name, Status) VALUES ('" + str(Plugin_Name) + "', '0')")
        except mariadb.Error as e: #Catcches errors and sends it to the bot log chan and user
            bot.notice(f"Error connecting to MariaDB Platform: {e}", sender_nick)
            bot.say(f"Error connecting to MariaDB Platform: {e}", "#tea-logs")        
        bot.notice("Unless any errors are seen it *SHOULD* have worked. Please check by typing '.dblist' (no quotes) and checking if the user has been added.", nick)

    def load_all_plugins(bot):
        cur = conn.cursor()
        cur.execute("SELECT Plugin_Name,Status FROM Enabled_Plugins")
        for (Plugin_Name,Status) in cur:
            if "Plugin Name: {Plugin_Name}, Status: {Status}" != "Plugin Name: , Status: ":
                if Status == 0:
                    #load the plugin here
                    cur.execute("update Enabled_Plugins set status=1 where Plugin_Name='" + str(Plugin_Name) + "'")

    def get_plugins(bot, nick):
        global cur
        cur = conn.cursor()
        cur.execute("SELECT Plugin_Name,Status FROM Enabled_Plugins")
        for (Plugin_Name, Status) in cur:
            if "Plugin Name: {Plugin_Name}, Status: {Status}" != "Plugin Name: , Status: ":
                if Status == 1:
                    Status = 'ON'
                else:
                    Status = 'OFF'
                bot.notice("Plugin Name: " + Plugin_Name + " | Status: " + Status, nick)

    def remove_plugin(remove_plugin, sender_nick, bot, trigger):
        global cur
        cur = conn.cursor()
        try:
            cur.execute(
                "DELETE FROM Enabled_Plugins WHERE Plugin_Name='" + remove_plugin + "'")
        except mariadb.Error as e:
            bot.notice(f"Error connecting to MariaDB Platform: {e}", sender_nick)
            bot.say(f"Error connecting to MariaDB Platform: {e}", "#tea-logs")
        bot.notice("Done! Please check that it did remove the plugin by typing '.showplugins' no quotes.", sender_nick)

@module.commands('addplugin')
def add_plugin_command(bot, trigger):
    db.connect(bot)
    nick = trigger.group(2)
    add_plugin_name = trigger.group(3)
    if not nick:
        nick = trigger.nick
    db.add_plugin(bot, nick, add_plugin_name)
    conn.close()

@module.commands('removeplugin')
def addplugin(bot, trigger):
    db.connect(bot)
    nick = trigger.group(2)
    remove_plugin = trigger.group(3)
    if not nick:
        nick = trigger.nick
    db.remove_plugin(remove_plugin, nick, bot, trigger)
    conn.close()

@module.commands('showplugins')
def showplugins(bot, trigger):
    db.connect(bot)
    nick = trigger.group(2)
    if not nick:
        nick = trigger.nick
    db.get_plugins(bot, nick)
    conn.close()

@module.interval(120)
def loadall(bot):
    db.connect(bot)
    db.load_all_plugins(bot)
    conn.close()
