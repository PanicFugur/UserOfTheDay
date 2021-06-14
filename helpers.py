from datetime import datetime, timedelta
import database


def hasItBeenADay(dateToCheck):
    now = datetime.now()
    if now < (dateToCheck + timedelta(hours=24)):
        return False
    else:
        return True


def getYesterday():
    now = datetime.now()
    yesterday = now - timedelta(hours=25)
    return yesterday


def isUserRegistered(tUserId, tChatId):
    db = database.DB('example.db')
    user = db.get_active_user(tUserId, tChatId)
    if user:
        return True
    else:
        return False


def mention(tUserName, tUserId):
    result = '['+tUserName+'](tg://user?id='+str(tUserId)+')'
    return result


def getStatString(item):
    return ' \n ' + str(item.count) + '\. ' + mention(item.tUserName,
                                                      item.tUserId)


def xstr(s):
    if s is None:
        return ''
    return str(s)


def concatUserNameFromUpdate(update):
    result = update.effective_user.first_name + ' ' \
         + xstr(update.effective_user.last_name)
    return result
