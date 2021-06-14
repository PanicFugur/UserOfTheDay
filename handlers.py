# -*- coding: UTF-8 -*-
from database import DB
import random
import helpers
import config


def reg(update, context):
    database = DB(config.DBPATH)
    userFLname = helpers.concatUserNameFromUpdate(update)
    database.add_user(update.effective_user.id,
                      userFLname,
                      update.effective_chat.id)
    user = update.effective_user
    context.bot.send_message(
        update.effective_chat.id,
        fr'Вы в игре, {user.mention_markdown_v2()}\!',
        parse_mode='MarkdownV2'
        )


def delete(update, context):
    database = DB(config.DBPATH)
    database.deactivate_user(update.effective_user.id,
                             update.effective_chat.id)
    user = update.effective_user
    context.bot.send_message(
        update.effective_chat.id,
        fr'Вы выбыли из игры, {user.mention_markdown_v2()}\!',
        parse_mode='MarkdownV2'
        )


def run(update, context):
    database = DB(config.DBPATH)
    chatId = update.effective_chat.id
    # Check if user's registered
    if helpers.isUserRegistered(update.effective_user.id, chatId):
        last_log = database.get_last_log(chatId)
        # Pull the last log to check if 24 hours has passed
        # if no last log found just get a date 25 hours before
        # a shit hack but it works
        if last_log is None:
            last_log_date = helpers.getYesterday()  # TODO Change it maybe
        else:
            last_log_date = last_log.timestamp
        if helpers.hasItBeenADay(last_log_date):
            userlist = database.get_users(chatId)  # get a list of active users
            if len(userlist) > 0:  # check that users exist
                notbeedor = userlist[random.randint(0, len(userlist) - 1)]
                beedor = userlist[random.randint(0, len(userlist) - 1)]
                # save logs of the selection
                database.add_log(notbeedor.id, chatId, False)
                database.add_log(beedor.id, chatId, True)
                context.bot.send_message(
                    update.effective_chat.id,
                    '🅱️идор дня: ' + helpers.mention(beedor.tUserName,
                                                     beedor.tUserId),
                    parse_mode='MarkdownV2'
                    )
                context.bot.send_message(
                    update.effective_chat.id,
                    'Красавчик дня: ' + helpers.mention(notbeedor.tUserName,
                                                        notbeedor.tUserId),
                    parse_mode='MarkdownV2'
                    )
            else:
                context.bot.send_message(chatId,
                                         'Пользователей не зарегистрировано')
        else:
            context.bot.send_message(chatId, 'Сегодня уже крутили барабан!')
    else:
        context.bot.send_message(chatId, 'Вы не зарегистрированы /reg')


def stat(update, context):
    database = DB(config.DBPATH)
    chat_id = update.effective_chat.id
    beedors = database.get_stats(chat_id, True)
    krasavchiks = database.get_stats(chat_id, False)
    # a little slow but it effectively solves the problem
    # of having number of records on each side unequal
    # TODO find a better solution for this
    beedors_str = '🅱️идоры:'
    for item in beedors:
        beedors_str = beedors_str + helpers.getStatString(item)
    krasavchiks_str = 'Красавчики:'
    for item in krasavchiks:
        krasavchiks_str = krasavchiks_str + helpers.getStatString(item)
    context.bot.send_message(chat_id, beedors_str, parse_mode='MarkdownV2')
    context.bot.send_message(chat_id, krasavchiks_str, parse_mode='MarkdownV2')
