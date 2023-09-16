import openpyxl
import os.path
import datetime
import pytz
from datetime import timedelta
from sqlighter import SQLighter
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, PollAnswer, InputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler


TOKEN = os.getenv('TOKEN')
group_id = os.getenv('group_id')
discount = 120
timezone = pytz.timezone("Europe/Moscow")
caption_text = "Что будете заказывать?\nПомощь: /help"
db = SQLighter('database.db')
scheduler = AsyncIOScheduler()


bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)

async def on_startup(_):
    for i in db.get_admins():
        try:
            await bot.send_message(chat_id=i[0], text=f"Бот был перезапущен {datetime.datetime.now(timezone)}")
        except Exception as e:
            pass
    print('Бот запущен!')

back_blk = InlineKeyboardButton(text='<Назад', callback_data='block_menu')
ib_adm = InlineKeyboardButton(text='<Назад', callback_data='admin')
previous = InlineKeyboardButton(text="<Назад", callback_data="previous")
ikb_short = InlineKeyboardMarkup(row_width=2)
ikb_short2 = InlineKeyboardMarkup(row_width=2)
ikb_special = InlineKeyboardMarkup(row_width=2)
ikb = InlineKeyboardMarkup(row_width=2)
ib_a = InlineKeyboardButton(text='Боулы', callback_data='Боулы')
ib_b = InlineKeyboardButton(text='Fast Food', callback_data='Fast Food')
ib_c = InlineKeyboardButton(text='Горячие блюда', callback_data='Горячие блюда')
ib_d = InlineKeyboardButton(text='Паста', callback_data='Паста')
ib_e = InlineKeyboardButton(text='Мучные блюда', callback_data='Мучные блюда')
ib_f = InlineKeyboardButton(text='Роллы', callback_data='Роллы')
ib_g = InlineKeyboardButton(text='Пиццы', callback_data='Пиццы')
ib_h = InlineKeyboardButton(text='Салаты', callback_data='Салаты')
ib_i = InlineKeyboardButton(text='Напитки', callback_data='Напитки')
ib_j = InlineKeyboardButton(text='Супы', callback_data='Супы')
ib1 = InlineKeyboardButton(text='Коллективный заказ', callback_data='group_order')
ib2 = InlineKeyboardButton(text='Мои заказы', callback_data='my_orders')
ib_admin = InlineKeyboardButton(text='Админ меню', callback_data='admin')
ikb.add(ib_c, ib_e, ib_a, ib_b, ib_d, ib_h, ib_g, ib_f, ib_i, ib_j).add(ib1).add(ib2)
ikb_special.add(ib_c, ib_e, ib_a, ib_b, ib_d, ib_h, ib_g, ib_f, ib_i, ib_j).add(ib1).add(ib2).add(ib_admin)
ikb_short.add(ib_c, ib_e, ib_a, ib_b, ib_d, ib_h, ib_g, ib_f, ib_i, ib_j).add(previous)
ikb_short2.add(ib_c, ib_e, ib_a, ib_b, ib_d, ib_h, ib_g, ib_f, ib_i, ib_j).add(ib_adm)

ikb_orders = InlineKeyboardMarkup(row_width=1)
ord_month = InlineKeyboardButton(text='Заказы за текущий месяц', callback_data='month_orders')
ord_cancel = InlineKeyboardButton(text='Отменить обед на сегодня', callback_data='cancel')
ikb_orders.add(ord_month, ord_cancel, previous)

ibadm1 = InlineKeyboardButton(text='🔒 Блокировка блюд', callback_data='block_menu')
ibadm2 = InlineKeyboardButton(text='🚷 Блокировка пользователей', callback_data='deact_user')
ibadm3 = InlineKeyboardButton(text='⚙ Редактирование пользователей', callback_data='ch_user')
ibadm4 = InlineKeyboardButton(text='🤴🏻 Назначение админов', callback_data='set_adm')
ibadm5 = InlineKeyboardButton(text='📆 Сегодняшний отчёт по заказам', callback_data='day_report')
ibadm6 = InlineKeyboardButton(text='🗓 Месячный отчет по заказам', callback_data='month_report')
ibadm7 = InlineKeyboardButton(text='⏹ Остановить опрос', callback_data='stop_poll')
ibadm8 = InlineKeyboardButton(text='↗ Отправить опрос', callback_data='send_poll')
ibadm9 = InlineKeyboardButton(text='🟢 Отключить прием заказов', callback_data='bot_activity')
ibadm10 = InlineKeyboardButton(text='🔴 Включить прием заказов', callback_data='bot_activity')

months = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

def get_last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - timedelta(days=1)


async def send_day_report(chat_id):
    filename = f"./Day_reports/FTobedbot_{datetime.datetime.now(timezone).strftime('%d_%m_%Y')}.xlsx"
    book = openpyxl.open("example.xlsx")
    sheet = book.worksheets[0]
    s = 2
    for i in db.get_day_report():
        sheet[s][0].value = i[0]
        sheet[s][1].value = i[1]
        sheet[s][2].value = i[2]
        sheet[s][3].value = db.get_user(i[3])[0][7]
        if db.get_user(i[3]):
            sheet[s][4].value = db.get_user(i[3])[0][5]
        else:
            sheet[s][4].value = i[3]
        if db.get_user(i[4]):
            sheet[s][5].value = db.get_user(i[4])[0][5]
        else:
            sheet[s][5].value = i[4]
        if db.get_user(i[5]):
            sheet[s][6].value = db.get_user(i[5])[0][5]
        else:
            sheet[s][6].value = i[5]
        sheet[s][7].value = i[6]
        s += 1
    book.save(filename)
    book.close()
    file = open(filename, 'rb')
    await bot.send_document(chat_id=chat_id, document=InputFile(file, filename=filename), caption="Список заказов на сегодня.")

async def send_month_report(chat_id, month):
    filename = f"./Month_reports/FTobedbot_{f'0{month}'[-2:]}_{datetime.datetime.now(timezone).strftime('%Y')}.xlsx"
    book = openpyxl.open("example.xlsx")
    sheet = book.worksheets[0]
    s = 2
    for i in db.get_month_report(f'0{month}'[-2:]):
        sheet[s][0].value = i[0]
        sheet[s][1].value = i[1]
        sheet[s][2].value = i[2]
        sheet[s][3].value = db.get_user(i[3])[0][7]
        if db.get_user(i[3]):
            sheet[s][4].value = db.get_user(i[3])[0][5]
        else:
            sheet[s][4].value = i[3]
        if db.get_user(i[4]):
            sheet[s][5].value = db.get_user(i[4])[0][5]
        else:
            sheet[s][5].value = i[4]
        if db.get_user(i[5]):
            sheet[s][6].value = db.get_user(i[5])[0][5]
        else:
            sheet[s][6].value = i[5]
        sheet[s][7].value = i[6]
        s += 1
    book.save(filename)
    book.close()
    file = open(filename, 'rb')
    await bot.send_document(chat_id=chat_id, document=InputFile(file, filename=filename), caption=f"Список заказов на {months[int(month)]}.")

async def send_poll():
     if db.bot_active():
        short_menu = []
        short_menu_ids = []
        db.empty_short_menu()
        for i in db.generate_short_menu():
            short_menu.append(i[0] + ' - ' + str(i[1]) + ' р')
            short_menu_ids.append(i[2])
        poll_info = await bot.send_poll(question='Выберите себе обед на сегодня!\n\nНаиболее популярные блюда:',
                                        options=short_menu,
                                        is_anonymous=False,
                                        protect_content=True,
                                        allows_multiple_answers=True,
                                        chat_id=group_id,
                                        reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Полное меню',
                                                                                                     url="t.me/ftobedbot")))
        db.add_short_menu(poll_info.message_id, poll_info.poll.id, short_menu_ids[0], short_menu_ids[1],
                          short_menu_ids[2], short_menu_ids[3], short_menu_ids[4], short_menu_ids[5],
                          short_menu_ids[6], short_menu_ids[7], short_menu_ids[8], short_menu_ids[9])


async def stop_poll():
    await bot.stop_poll(group_id, db.get_short_menu()[10])


async def group_order(clb_user_id, chat_id, message_id, clg_names):
    ikb_colleague = InlineKeyboardMarkup(row_width=1)
    ikb_colleague.add(InlineKeyboardButton(text="Себе", callback_data=clb_user_id))
    for i in db.get_users_except_me(user_id=clb_user_id):
        if i[6]:
            ikb_colleague.add(InlineKeyboardButton(text=f'{i[5]}, {i[7]}', callback_data=i[0]))
    ikb_colleague.add(InlineKeyboardButton(text='🍽 Выбрать блюдо', callback_data='choose'))
    ikb_colleague.add(previous)
    await bot.edit_message_caption(caption=f'<b>Коллективный заказ:</b>\n\nКому: {clg_names}',
                                   chat_id=chat_id, message_id=message_id,
                                   reply_markup=ikb_colleague)


async def list_menu(menu_category, chat_id, message_id):
    ikb_list_menu = InlineKeyboardMarkup(row_width=1)
    for i in db.get_all_menu(category=menu_category):
        stick = ''
        if not i[4]:
            stick = '❌'
        ikb_list_menu.add(InlineKeyboardButton(text=f'{stick} {i[2]} - {i[3]} р', callback_data=i[0]))
    ikb_list_menu.add(back_blk)
    await bot.edit_message_caption(caption=f'<b>{menu_category}</b>', chat_id=chat_id, message_id=message_id, reply_markup=ikb_list_menu)


async def list_users(user_id, caption_txt, chat_id, message_id):
    state = db.get_user(user_id)[0][8]
    ikb_list_users = InlineKeyboardMarkup(row_width=1)
    for i in db.get_users_except_me(user_id=0):
        stick = ''
        if i[6] and state == 'deact_user':
            stick = stick + '✅'
        elif not i[6] and state == 'deact_user':
            stick = stick + '❌'
        if i[12]:
            stick = stick + ' 👑'
        ikb_list_users.add(InlineKeyboardButton(text=f'{stick} {i[5]}, {i[7]}', callback_data=i[0]))
    ikb_list_users.add(ib_adm)
    await bot.edit_message_caption(caption=caption_txt,
                                   chat_id=chat_id, message_id=message_id,
                                   reply_markup=ikb_list_users)


async def main_menu(user_id, chat_id, message_id):
    if db.is_admin(user_id):
        await bot.edit_message_caption(caption='<b><em>' + caption_text + '</em></b>',
                                       chat_id=chat_id,
                                       message_id=message_id,
                                       reply_markup=ikb_special)
    else:
        await bot.edit_message_caption(caption='<b><em>' + caption_text + '</em></b>',
                                       chat_id=chat_id,
                                       message_id=message_id, reply_markup=ikb)


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def handler_new_member(message: types.Message):
    for user in message.new_chat_members:
        if not user.is_bot:
            db.add_user(user.id, user.first_name,
                        user.last_name, user.username,
                        user.first_name, True)
            for admin in db.get_admins():
                await bot.send_message(admin[0], f'В группу добавлен пользователь:\n\n{str(user)}')


# @dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER)
# async def handler_left_member(message: types.Message):
#     db.del_user(message.left_chat_member.id)


@dp.message_handler(commands=['start'])
async def send_kb(message: types.Message):
    db.set_user_state(message.from_user.id, '')
    member = await bot.get_chat_member(group_id, message.from_user.id)
    if (member.status == 'member' or member.status == 'creator' or member.status == 'owner' or member.status == 'administrator') and \
            db.user_active(message.from_user.id):
        if db.is_admin(message.from_user.id):
            await bot.send_photo(chat_id=message.from_user.id,
                                 photo="https://bigpicture.ru/wp-content/uploads/2018/11/saltbae_salt1_index1a.jpg",
                                 caption='<b><em>' + caption_text + '</em></b>', reply_markup=ikb_special)
        else:
            await bot.send_photo(chat_id=message.from_user.id,
                                 photo="https://bigpicture.ru/wp-content/uploads/2018/11/saltbae_salt1_index1a.jpg",
                                 caption='<b><em>' + caption_text + '</em></b>', reply_markup=ikb)
        # await message.delete()

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    info = f'''<b>Добро пожаловать!</b>\n\n<em>Скидка = {discount} р в день. (Оплачивает компания)</em>\n
    Заказы разбиты по категориям. Зайдя в категорию блюд, вы увидите список блюд с ценами.
    Заказать или отменить обед можно до 10:30. В 9:00 в группу придет опрос, через который также можно сделать заказ.
    Цены указаны без скидок. Скидка будет учтена автоматически. Сделанный заказ можно посмотреть или отменить в резделе "Мои заказы". Там же можно посмотреть список ваших заказов за текущий месяц и совокупную сумму с учетом всех скидок.
    Также вы можете сделать коллективный заказ, максимум на троих, соответственно скидка будет учитываться от каждого.
    В этом же разделе можно сделать заказ коллеге, выбрав его(их) в списке пользователей.
    При этом, те, для кого вы сделали заказ, получат сообщение об этом. Для того, чтобы бот работал правильно, необходимо обязательно нажать в нём Start.\n\nПриступим? /start'''
    await bot.send_message(chat_id=message.from_user.id, text=info)

@dp.message_handler(commands=['id'])
async def send_id(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=str(message.from_user))

@dp.message_handler(content_types='text')
async def handler_userdata(message: types.Message):
    if db.is_admin(message.from_user.id) and db.get_user(message.from_user.id)[0][8] == 'ch_user' and message.text.count('\n') == 1:
        before_newline, after_newline = message.text.split('\n')
        db.set_userdata(db.get_user(message.from_user.id)[0][9], before_newline, after_newline)
        await message.delete()
    else:
        pass


@dp.callback_query_handler()
async def vote_callback(callback: CallbackQuery):
    member = await bot.get_chat_member(group_id, callback.from_user.id)
    if (member.status == 'member' or member.status == 'creator' or member.status == 'owner' or member.status == 'administrator') \
            and db.user_active(callback.from_user.id):
        if callback.data == "group_order":
            if db.bot_active():
                db.set_user_state(callback.from_user.id, 'group')
                db.empty_selected_users(callback.from_user.id)
                await group_order(callback.from_user.id, callback.message.chat.id, callback.message.message_id, '')
                await callback.answer()
            else:
                await callback.answer(text='На данный момент заказы не принимаются.', show_alert=True)
        elif callback.data == "my_orders":
            my_orders = db.get_day_orders(callback.from_user.id)
            if bool(len(my_orders)):
                zakaz = ''
                for i in my_orders:
                    if i[7]:
                        us2 = f', {db.get_user(i[7])[0][5]}'
                    else:
                        us2 = ''
                    if i[8]:
                        us3 = f', {db.get_user(i[8])[0][5]}'
                    else:
                        us3 = ''
                    zakaz = zakaz + f"🟢 {i[4]}  {i[2]} - {str(i[3])} р ({db.get_user(i[6])[0][5]}{us2}{us3})\n"
                await bot.edit_message_caption(caption=f'<b>🛒 Ваши заказы на сегодня:</b>\n\n{str(zakaz)}\n<em>💵 Общая сумма с вычетом = <b>{str(db.get_day_sum(user_id=callback.from_user.id, discount=discount))} р</b></em>',
                                               chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                               reply_markup=ikb_orders)
            else:
                await bot.edit_message_caption(
                    caption='<b>🛒 Вы сегодня ничего не заказывали.</b>',
                    chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                    reply_markup=ikb_orders)
                await callback.answer()
        elif callback.data == "month_orders":
            my_orders = db.get_month_orders(callback.from_user.id)

            if bool(len(my_orders)):
                zakaz = ''
                for i in my_orders:
                    if i[7]:
                        us2 = f', {db.get_user(i[7])[0][5]}'
                    else:
                        us2 = ''
                    if i[8]:
                        us3 = f', {db.get_user(i[8])[0][5]}'
                    else:
                        us3 = ''
                    zakaz = zakaz + f"🟢 {i[4]}  {i[2]} - {str(i[3])} р ({db.get_user(i[6])[0][5]}{us2}{us3})\n"

                ikb_nazad = InlineKeyboardMarkup(row_width=1)
                ikb_nazad.add(previous)
                await bot.edit_message_caption(caption=f'<b>🛒 Ваши заказы в этом месяце:</b>\n\n{str(zakaz)}\n<em>💵 Общая сумма с вычетом = <b>{str(db.get_month_sum(user_id=callback.from_user.id, discount=discount))} р</b></em>',
                                               chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                               reply_markup=ikb_nazad)
                await callback.answer()
            else:
                await callback.answer("У вас нет заказов в этом месяце.", show_alert=True)
        elif callback.data == "cancel":
            if datetime.datetime.now(timezone).time() < datetime.time(10, 30, 0, 0):
                db.del_orders(callback.from_user.id)
                await callback.answer(text='Ваш обед на сегодня отменён.', show_alert=True)
                await bot.edit_message_caption(caption='<b>🛒 Вы сегодня ничего не заказывали.</b>',
                                               chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                               reply_markup=ikb_orders)
            else:
                await callback.answer(text='Поздно отменять!\n\nОтменить можно до 10:30', show_alert=True)

            # db.del_orders(callback.from_user.id)
            # await callback.answer(text='Ваш обед на сегодня отменён.', show_alert=True)
            # await bot.edit_message_caption(caption='<b>🛒 Вы сегодня ничего не заказывали.</b>',
            #                                chat_id=callback.message.chat.id, message_id=callback.message.message_id,
            #                                reply_markup=ikb_orders)
        elif callback.data == "previous":
            db.set_user_state(callback.from_user.id, None)
            db.empty_selected_users(callback.from_user.id)
            if db.is_admin(callback.from_user.id):
                await bot.edit_message_caption(caption=f'<b><em>{caption_text}</em></b>',
                                               chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                               reply_markup=ikb_special)
            else:
                await bot.edit_message_caption(caption=f'<b><em>{caption_text}</em></b>',
                                               chat_id=callback.message.chat.id,
                                               message_id=callback.message.message_id, reply_markup=ikb)
        elif callback.data in db.get_menu_category():
            if db.get_user(callback.from_user.id)[0][8] == 'block_menu':
                await list_menu(callback.data, callback.message.chat.id, callback.message.message_id)
                await callback.answer()
            else:
                ikb2 = InlineKeyboardMarkup(row_width=1)
                for i in db.get_menu(category=callback.data):
                    ikb2.add(InlineKeyboardButton(text=f'{i[2]} - {i[3]} р', callback_data=i[0]))
                ikb2.add(previous)
                await bot.edit_message_caption(caption=f'<b>{callback.data}</b>', chat_id=callback.message.chat.id,
                                               message_id=callback.message.message_id, reply_markup=ikb2)
                await callback.answer()
        elif callback.data in db.get_menu_ids():
            if db.get_user(callback.from_user.id)[0][8] == 'block_menu' and db.is_admin(callback.from_user.id):
                meal = db.get_meal(callback.data)
                db.set_block_menu(callback.data, not meal[0][4])
                await list_menu(meal[0][1], callback.message.chat.id, callback.message.message_id)
            elif db.get_user(callback.from_user.id)[0][8] == 'group' and datetime.datetime.now(timezone).time() < datetime.time(10, 30, 0, 0):
                if db.bot_active():
                    user_data = [db.get_user(callback.from_user.id)[0][9], db.get_user(callback.from_user.id)[0][10],
                                 db.get_user(callback.from_user.id)[0][11]]
                    usr = []
                    usr_names = []
                    for i in user_data:
                        if i is not None:
                            usr_names.append(db.get_user(int(i))[0][5])
                        else:
                            usr_names.append('')
                        if i is not None and int(i) != int(callback.from_user.id):
                            usr.append(i)
                    db.add_order(callback.from_user.id, callback.data, db.get_meal(callback.data)[0][2], db.get_meal(callback.data)[0][3], 'bot', for1=user_data[0], for2=user_data[1], for3=user_data[2])
                    if len(usr):
                        for i in usr:
                            try:
                                await bot.send_message(i, f'<b>{db.get_user(callback.from_user.id)[0][5]}</b> создал заказ:\n\n<b><em>{db.get_meal(callback.data)[0][2]} - {db.get_meal(callback.data)[0][3]} р</em></b>\n\nдля:\n   <em>{usr_names[0]}\n   {usr_names[1]}\n   {usr_names[2]}</em>\n\nПосмотреть или отменить заказ можно в разделе "Мои заказы".')
                            except Exception as e:
                                pass
                    db.set_user_state(callback.from_user.id, '')
                    await callback.answer(text=f"🛒 Заказ добавлен:\n\n🔸 {db.get_meal(callback.data)[0][2]} - {db.get_meal(callback.data)[0][3]} р\n\n💵 Общая сумма с вычетом = {str(db.get_day_sum(user_id=callback.from_user.id, discount=discount))} р\n\nВы можете отменить заказ до 10:30\n\nПриятного аппетита!", show_alert=True)
                    await main_menu(callback.from_user.id, callback.message.chat.id, callback.message.message_id)
                else:
                    await callback.answer(text='На данный момент заказы не принимаются.', show_alert=True)
            elif db.get_user(callback.from_user.id)[0][8] != 'group' and datetime.datetime.now(timezone).time() < datetime.time(10, 30, 0, 0):
                if db.bot_active():
                    db.add_order(callback.from_user.id, callback.data, db.get_meal(callback.data)[0][2], db.get_meal(callback.data)[0][3], 'bot',
                                 for1=callback.from_user.id, for2=None, for3=None)
                    await callback.answer(text=f"🛒 Заказ добавлен:\n\n🔸 {db.get_meal(callback.data)[0][2]} - {db.get_meal(callback.data)[0][3]} р\n\n💵 Общая сумма с вычетом = {str(db.get_day_sum(user_id=callback.from_user.id, discount=discount))} р\n\nВы можете отменить заказ до 10:30\n\nПриятного аппетита!", show_alert=True)
                    await main_menu(callback.from_user.id, callback.message.chat.id, callback.message.message_id)
                else:
                    await callback.answer(text='На данный момент заказы не принимаются.', show_alert=True)
            else:
                await callback.answer(text="На сегодня приём заказов окончен.", show_alert=True)
                await main_menu(callback.from_user.id, callback.message.chat.id, callback.message.message_id)
        elif callback.data == 'choose':
            user_data = [db.get_user(callback.from_user.id)[0][9], db.get_user(callback.from_user.id)[0][10],
                         db.get_user(callback.from_user.id)[0][11]]
            s = 0
            for i in user_data:
                if i is not None:
                    s += 1
            if db.get_user(callback.from_user.id)[0][8] == 'group':
                if s == 1:
                    await bot.edit_message_caption(caption='<b><em>Выберите заказ для коллеги:</em></b>',
                                               chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                               reply_markup=ikb_short)
                elif s > 1:
                    await bot.edit_message_caption(caption=f'<b><em>Выберите заказ на {s}-х:</em></b>',
                                               chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                               reply_markup=ikb_short)
                else:
                    await callback.answer(text='Выберите, кому хотите заказать.')
        elif callback.data == "admin":
            if db.is_admin(callback.from_user.id):
                db.set_user_state(callback.from_user.id, None)
                db.empty_selected_users(callback.from_user.id)
                ikb_adm = InlineKeyboardMarkup(row_width=1)
                if db.bot_active():
                    ikb_adm.add(ibadm9, ibadm1, ibadm2, ibadm3, ibadm4, ibadm5, ibadm6, ibadm7, ibadm8, previous)
                elif not db.bot_active():
                    ikb_adm.add(ibadm10, ibadm1, ibadm2, ibadm3, ibadm4, ibadm5, ibadm6, ibadm7, ibadm8, previous)
                await bot.edit_message_caption(caption='<b>Админ меню</b>', chat_id=callback.message.chat.id,
                                               message_id=callback.message.message_id, reply_markup=ikb_adm)
            else:
                db.set_user_state(callback.from_user.id, None)
                db.empty_selected_users(callback.from_user.id)
                await bot.edit_message_caption(caption=f'<b><em>{caption_text}</em></b>',
                                               chat_id=callback.message.chat.id,
                                               message_id=callback.message.message_id, reply_markup=ikb)
            await callback.answer()
        elif callback.data == "bot_activity":
            db.ch_bot_activity()
            if db.is_admin(callback.from_user.id):
                db.set_user_state(callback.from_user.id, None)
                db.empty_selected_users(callback.from_user.id)
                ikb_adm = InlineKeyboardMarkup(row_width=1)
                if db.bot_active():
                    ikb_adm.add(ibadm9, ibadm1, ibadm2, ibadm3, ibadm4, ibadm5, ibadm6, ibadm7, ibadm8, previous)
                elif not db.bot_active():
                    ikb_adm.add(ibadm10, ibadm1, ibadm2, ibadm3, ibadm4, ibadm5, ibadm6, ibadm7, ibadm8, previous)
                await bot.edit_message_caption(caption='<b>Админ меню</b>', chat_id=callback.message.chat.id,
                                               message_id=callback.message.message_id, reply_markup=ikb_adm)
            else:
                db.set_user_state(callback.from_user.id, None)
                db.empty_selected_users(callback.from_user.id)
                await bot.edit_message_caption(caption=f'<b><em>{caption_text}</em></b>',
                                               chat_id=callback.message.chat.id,
                                               message_id=callback.message.message_id, reply_markup=ikb)
            await callback.answer()
        elif callback.data == "block_menu":
            db.set_user_state(callback.from_user.id, 'block_menu')
            await bot.edit_message_caption(caption=f'<b><em>Выберите блюдо для блокировки:</em></b>',
                                           chat_id=callback.message.chat.id,
                                           message_id=callback.message.message_id, reply_markup=ikb_short2)
            await callback.answer()
        elif callback.data == "deact_user":
            db.set_user_state(callback.from_user.id, 'deact_user')
            await list_users(callback.from_user.id, '<b>Блокировка пользователей:</b>\n\n✅ - активен\n❌ - неактивен\n👑 - админ', callback.message.chat.id, callback.message.message_id)
            await callback.answer()
        elif callback.data == "ch_user":
            db.set_user_state(callback.from_user.id, 'ch_user')
            await list_users(callback.from_user.id, '<b>Для того, чтобы изменить имя и отдел, выберите пользователя:</b>', callback.message.chat.id, callback.message.message_id)
            await callback.answer()
        elif callback.data == "set_adm":
            db.set_user_state(callback.from_user.id, 'set_adm')
            await list_users(callback.from_user.id, '<b>Назначить или разжаловать администраторов бота:</b>\n\n👑 - админ', callback.message.chat.id, callback.message.message_id)
            await callback.answer()
        elif callback.data == 'stop_poll':
            await stop_poll()
            await callback.answer(text='Опрос в группе закрыт.', show_alert=True)
        elif callback.data == 'send_poll':
            await send_poll()
            await callback.answer(text='Отправлен опрос в группу.', show_alert=True)
        elif callback.data == "day_report":
            await send_day_report(callback.from_user.id)
            await callback.answer()
        elif callback.data == "month_report":
            ikb_months = InlineKeyboardMarkup(row_width=1)
            for i in range(1, datetime.datetime.now(timezone).month + 1):
                ikb_months.add(InlineKeyboardButton(text=f'{months[i]}', callback_data=str(i)))
            ikb_months.add(ib_adm)
            await bot.edit_message_caption(caption=f'<b><em>За какой месяц хотите получить отчёт?</em></b>',
                                           chat_id=callback.message.chat.id,
                                           message_id=callback.message.message_id, reply_markup=ikb_months)
            await callback.answer()
        elif callback.data.isdigit() and int(callback.data) in range(1, 13):
            await send_month_report(callback.from_user.id, callback.data)
            await callback.answer()
        elif callback.data.isdigit() and int(callback.data) in db.get_users_ids():
            colleagues = db.get_users_ids()
            if db.get_user(callback.from_user.id)[0][8] == 'group':
                user_data = [db.get_user(callback.from_user.id)[0][9], db.get_user(callback.from_user.id)[0][10],
                             db.get_user(callback.from_user.id)[0][11]]
                if None in user_data and (int(callback.data) in colleagues) and callback.data not in user_data:
                    for i in range(3):
                        user_data = [db.get_user(callback.from_user.id)[0][9], db.get_user(callback.from_user.id)[0][10],
                                     db.get_user(callback.from_user.id)[0][11]]
                        if user_data[i] is None:
                            if callback.data not in user_data:
                                db.set_sel_user(callback.from_user.id, callback.data, i + 1)
                    user_data = [db.get_user(callback.from_user.id)[0][9], db.get_user(callback.from_user.id)[0][10],
                                 db.get_user(callback.from_user.id)[0][11]]
                    sel_users = ", ".join([db.get_user(x)[0][5] for x in user_data if x is not None])
                    await group_order(callback.from_user.id, callback.message.chat.id,
                                      callback.message.message_id, sel_users)
                elif callback.data in user_data:
                    await callback.answer(text="Уже выбран!")
                else:
                    await callback.answer(text="Вы можете добавить максимум 3 человека.")
            elif db.get_user(callback.from_user.id)[0][8] == 'deact_user' and db.is_admin(callback.from_user.id):
                if int(callback.data) == int(callback.from_user.id):
                    await callback.answer(text='Нельзя заблокировать самого себя. У вас не будет возможности это исправить.', show_alert=True)
                else:
                    db.set_active(callback.data, not db.get_user(callback.data)[0][6])
                    await list_users(callback.from_user.id,
                                     '<b>Блокировка пользователей:</b>\n\n✅ - активен\n❌ - неактивен\n👑 - админ',
                                     callback.message.chat.id, callback.message.message_id)
                    await callback.answer()
            elif db.get_user(callback.from_user.id)[0][8] == 'set_adm' and db.is_admin(callback.from_user.id):
                if int(callback.data) == int(callback.from_user.id):
                    await callback.answer(text='Нельзя снять полномочия с самого себя. У вас не будет возможности это исправить.', show_alert=True)
                else:
                    db.set_admin(callback.data, not db.get_user(callback.data)[0][12])
                    await list_users(callback.from_user.id,
                                     '<b>Назначить или разжаловать администраторов бота:</b>\n\n👑 - админ',
                                     callback.message.chat.id, callback.message.message_id)
                    await callback.answer()
            elif db.get_user(callback.from_user.id)[0][8] == 'ch_user' and db.is_admin(callback.from_user.id):
                db.set_sel_user(callback.from_user.id, callback.data, 1)
                ikb_ch_user = InlineKeyboardMarkup(row_width=1)
                ikb_ch_user.add(ibadm3)
                await bot.edit_message_caption(caption=f'<b><em>Отправьте ФИО и Отдел в виде:\n\n</em></b>Иванов И.И.\nТехподдержка\n\nВыбран пользователь: {db.get_user(callback.data)[0][1]}',
                                               chat_id=callback.message.chat.id,
                                               message_id=callback.message.message_id, reply_markup=ikb_ch_user)
                await callback.answer()
        else:
            await callback.answer('Ошибка!')
    else:
        await callback.answer(text='Вы не можете пользоваться ботом.', show_alert=True)


@dp.poll_answer_handler()
async def handle_poll_answer(poll: PollAnswer):
    if db.user_active(poll.user.id) and datetime.datetime.now(timezone).time() < datetime.time(10, 30, 0, 0):
        if poll.option_ids:
            for i in poll.option_ids:
                db.add_order(poll.user.id, db.get_short_menu()[i], db.get_meal(db.get_short_menu()[i])[0][2],
                             db.get_meal(db.get_short_menu()[i])[0][3], 'poll', poll.user.id, None, None)
        else:
            db.del_poll_orders(poll.user.id)
    else:
        try:
            await bot.send_message(chat_id=poll.user.id, text='Вы не можете заказать обед, ваш голос не будет учтён.')
        except Exception as e:
            pass

days = 'mon,tue,wed,thu,fri'  # Будние дни

# last_day_of_month = get_last_day_of_month(datetime.datetime.now(timezone))
# run_time = datetime.time(10, 31)
# run_date = datetime.datetime.combine(last_day_of_month.date(), run_time)
day_rep_user = os.getenv('dr_user')
month_rep_user = os.getenv('mr_user')

# Создаем задачи
scheduler.add_job(func=send_poll, trigger='cron', day_of_week=days, hour=9, minute=0,  timezone='Europe/Moscow')
scheduler.add_job(func=stop_poll, trigger='cron', day_of_week=days, hour=10, minute=30, timezone='Europe/Moscow')
scheduler.add_job(func=send_day_report, trigger='cron', day_of_week=days, hour=10, minute=31, timezone='Europe/Moscow', args=[day_rep_user])
scheduler.add_job(func=send_month_report, trigger='cron', day='last', hour=10, minute=35, timezone='Europe/Moscow', args=[month_rep_user, datetime.datetime.now().strftime('%m')])

# Запускаем планировщик задач
scheduler.start()

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
