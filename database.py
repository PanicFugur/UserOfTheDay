from peewee import IntegerField, TextField, BooleanField, DateTimeField,\
     Model, SqliteDatabase, DoesNotExist, JOIN, fn, ForeignKeyField
import datetime
import os
import config

# TODO this is a bad hack, fix it later
db = SqliteDatabase(config.DBPATH)


# Model definition
class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    tUserId = IntegerField()
    tUserName = TextField()
    tChatId = IntegerField()
    active = BooleanField(default=True)


class Logs(BaseModel):
    UserId = ForeignKeyField(User)
    tChatId = IntegerField()
    beeDor = BooleanField(default=True)
    timestamp = DateTimeField(default=datetime.datetime.now)


class Resource(BaseModel):
    tResId = IntegerField()
    resType = TextField()
    beeDor = BooleanField() 


# Database class definition, for handling all database related nonsense
class DB:

    def __checkdb(self, dbpath):
        '''Check if database file exists'''
        isDBPresent = False
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

    def add_user(self, tUserId, tUserName, tChatId):
        # First try to find the User in userlist
        try:
            newUser = User.get(User.tUserId == tUserId,
                               User.tChatId == tChatId)
            newUser.tUserName = tUserName
            newUser.active = True
        # If exception thrown then User is asbsent, so just create a new one
        except (Exception):
            print('No User, creating')
            newUser = User(tUserId=tUserId,
                           tUserName=tUserName, tChatId=tChatId)
        # Regardless of the path, save the record,
        # if it has primary key ID as in case of existing user
        # it will Update the record to reactivate the User
        newUser.save()

    def deactivate_user(self, tUserId, tChatId):
        # Look for User first cause if he's not in the database
        # we're gonna get an exception
        # if User's found just set his active flag to false and save
        try:
            user = User.get(User.tUserId == tUserId, User.tChatId == tChatId)
            user.active = False
            user.save()
            return True
        except (Exception):
            print('Ooops User has never been registered')
            return False

    def get_users(self, tChatId, searchByActiveFlag=True):
        '''
        Search User table for Users in a specified chat

        Specify whether you want to see only active users by passing
        searchByActiveFlag parameter if not passed
        it will default to looking only for active Users
        '''
        if searchByActiveFlag is False:
            users = User.select().where(User.tChatId == tChatId)
        else:
            users = User.select().where(User.tChatId == tChatId,
                                        User.active == True)
# TODO flake8 keeps moaning about using IS in bool comparisons
# but that breaks the query and returns garbage
# research how to fix that
        return users

    def get_active_user(self, tUserId, tChatId):
        try:
            user = User.get(User.tUserId == tUserId,
                            User.tChatId == tChatId,
                            User.active == True)
# TODO flake8 keeps moaning about using IS in bool comparisons
# but that breaks the query and returns garbage
# research how to fix that
            return user
        except(DoesNotExist):
            return None

    def add_log(self, UserId, tChatId, beeDor):
        """Insert a new beedor/not beedor selection into Logs table """
        newLog = Logs(UserId=UserId, tChatId=tChatId, beeDor=beeDor)
        newLog.save()

    def get_last_log(self, ChatId):
        try:
            lastLog = Logs.select().where(Logs.tChatId == ChatId).\
                      order_by(Logs.timestamp.desc()).get()
            return lastLog
        except(DoesNotExist):
            return None

    def get_stats(self, ChatId, beeDor):
        """Gets count of logs for each registered user in the chat with flag"""
        # The query in this next step is long and convoluted
        # but it needs to be that way
        # so we don't have to do filtering
        # on the app side and let sqlite + peewee do their thing
        counts = (User
                  .select(User, fn.Count(Logs.id).alias('count'))
                  .where(User.tChatId == ChatId, Logs.beeDor == beeDor)
                  .join(Logs, JOIN.LEFT_OUTER)
                  .group_by(User)
                  .order_by(fn.Count(Logs.id).desc()))
        return counts

    def add_res(self, tResId, resType, beedor):
        newRes = Resource(tResId=tResId, resType=resType, beedor=beedor)
        newRes.save()

    def get_ress(self, beedor):
        resList = Resource.select().where(beedor=beedor)
        return resList
