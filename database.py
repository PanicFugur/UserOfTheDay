from peewee import *
import datetime
import os

#TODO this is a bad hack, fix it later with enviroment variables or something
db = SqliteDatabase('example.db')

#Model definition
class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    tUserId = IntegerField()
    tChatId = IntegerField()
    active = BooleanField(default=True)

class Logs(BaseModel):
    UserId = ForeignKeyField(User)
    beeDor = BooleanField(default=True)
    timestamp = DateTimeField(default=datetime.datetime.now)

        
#Database class definition, for handling all database related nonsense
class DB:

    def __checkdb(self, dbpath):
        '''Check if database file exists'''
        isDBPresent= False
        for file in os.listdir(os.path.curdir):
            if file == dbpath:
                isDBPresent = True
        return isDBPresent

    def __createdb(self):
        '''Create database file and tables from models'''
        self.db.connect()
        self.db.create_tables([User, Logs])
    
    
    def __init__(self, dbpath):
        self.db = SqliteDatabase(dbpath)
        if not self.__checkdb(dbpath):
            self.__createdb()

    def __convertResult(self, queryRes):
        pass

    def add_user(self, tUserId, tChatId):
        #First try to find the User in userlist
        try:
            newUser = User.get(User.tUserId == tUserId, User.tChatId == tChatId)
            newUser.active = True
        #If exception thrown then User must be asbsent, so just create a new one
        except:
            print('No User, creating')
            newUser = User(tUserId = tUserId, tChatId =  tChatId)
        #Regardless of the path, save the record, if it has primary key ID as in case of existing user
        #it will Update the record to reactivate the User
        newUser.save()


    def deactivate_user(self, tUserId, tChatId):
        #Look for User first cause if he's not in the database
        #we're gonna get an exception
        #if User's found just set his active flag to false and save
        try:
            user = User.get(User.tUserId == tUserId, User.tChatId == tChatId)
            user.active = False
            user.save()
            return True
        except:
            print('Ooops User has never been registered')
            return False

    def get_users(self, tChatId, searchByActiveFlag = True):
        '''
        Search User table for Users in a specified chat

        Specify whether you want to see only active users by passing searchByActiveFlag parameter
        if not passed it will default to looking only for active Users
        '''
        if searchByActiveFlag == False:
                users = User.select().where(User.tChatId == tChatId)
        else:
                users = User.select().where(User.tChatId == tChatId, User.active == True)
        return users

    def add_log(self, UserId, beeDor):
        """Insert a new beedor/not beedor selection into Logs table """
        newLog = Logs(UserId = UserId, beeDor = beeDor)
        newLog.save()
    
    def get_stats(self, ChatId, beeDor):
        """Gets count of logs for each registered user in the chat with beedor flag"""
        #The query in this next step is long and convoluted but it needs to be that way
        #so we don't have to do filtering on the app side and let sqlite + peewee do their thing
        counts = (User
                    .select(User, fn.Count(Logs.id).alias('count'))
                    .where(User.tChatId == ChatId, Logs.beeDor == beeDor)
                    .join(Logs, JOIN.LEFT_OUTER)
                    .group_by(User))
        return counts
    

        

if __name__ == '__main__':
    db = DB('example.db')

