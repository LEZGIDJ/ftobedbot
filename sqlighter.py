import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def user_active(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT `active` FROM `users` WHERE `id` = ?', (user_id,)).fetchone()
            if result:
                return result[0]
            else:
                return False

    def is_admin(self, user_id):
        """Проверяем, является ли юзер админом"""
        with self.connection:
            result = self.cursor.execute('SELECT `admin` FROM `users` WHERE `id` = ?', (user_id,)).fetchone()
            return bool(result[0])

    def bot_active(self):
        """Проверяем активацию бота"""
        with self.connection:
            result = self.cursor.execute('SELECT `active` FROM `bot_active`;').fetchone()
            return bool(result[0])

    def ch_bot_activity(self):
        with self.connection:
            return self.cursor.execute(
                'UPDATE `bot_active` SET active = CASE WHEN active = 1 THEN 0 ELSE 1 END;')

    def get_users_except_me(self, user_id):
        """Получить список всех сотрудников кроме user_id"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM `users` WHERE `id` <> ? ORDER BY `department`;', (user_id,)).fetchall()

    def get_menu(self, category):
        """Получить меню"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM `menu` WHERE `category` = ? AND `active` IS TRUE ORDER BY `price` DESC;', (category, )).fetchall()

    def get_all_menu(self, category):
        """Получить меню"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM `menu` WHERE `category` = ? ORDER BY `price` DESC;', (category, )).fetchall()

    def get_meal(self, meal_id):
        """Получить блюдо"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM `menu` WHERE `id` = ?;', (meal_id,)).fetchall()

    def get_menu_category(self):
        """Получить меню"""
        with self.connection:
            zapros = self.cursor.execute('SELECT `category` FROM `menu` GROUP BY `category`;').fetchall()
            menu_cat = []
            for i in zapros:
                menu_cat.append(i[0])
            return menu_cat

    def get_menu_ids(self):
        """Получить список блюд"""
        with self.connection:
            zapros = self.cursor.execute('SELECT `id` FROM `menu`;').fetchall()
            menu = []
            for i in zapros:
                menu.append(i[0])
            return menu

    def add_user(self, id, first_name, last_name, username, given_name, active):
        """Добавляем пользователя"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (id, first_name, last_name, username, date, given_name, active, department, state, selected_user1, selected_user2, selected_user3, admin) VALUES(?,?,?,?, datetime('now', 'localtime'),?,?,?,?,?,?,?,?);", (id, first_name, last_name, username, given_name, active, None, None, None, None, None, None))

    def del_user(self, id):
        """Удаляем пользователя"""
        with self.connection:
            return self.cursor.execute('DELETE FROM `users` WHERE id = ?;', (id,))

    def add_order(self, user_id, order_id, name, price, order_from, for1, for2, for3):
        """Добавляем заказ"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `orders` (`user_id`, `order_id`, `name`, `price`, `date`, `order_from`, `order_for_1`, `order_for_2`, `order_for_3`) VALUES(?,?,?,?, date('now', 'localtime'),?,?,?,?);", (user_id, order_id, name, price, order_from, for1, for2, for3))

    def del_orders(self, user_id):
        """Удаляем сегодняшние заказы"""
        with self.connection:
            return self.cursor.execute("DELETE FROM `orders` WHERE (`order_for_1` = ? OR `order_for_2` = ? OR `order_for_3` = ?) AND `date` = date('now', 'localtime');", (user_id, user_id, user_id))

    def get_day_orders(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM (SELECT * FROM `orders` WHERE `date` BETWEEN date('now', 'localtime') AND date('now', 'localtime')) WHERE (`order_for_1` = ? OR `order_for_2` = ? OR `order_for_3` = ?)", (user_id, user_id, user_id)).fetchall()

    def get_month_orders(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM (SELECT * FROM `orders` WHERE `date` BETWEEN date('now', 'start of month', 'localtime') AND date('now', 'localtime')) WHERE (`order_for_1` = ? OR `order_for_2` = ? OR `order_for_3` = ?)", (user_id, user_id, user_id)).fetchall()

    def add_short_menu(self, message_id, poll_id, ord0, ord1, ord2, ord3, ord4, ord5, ord6, ord7, ord8, ord9):
        """Добавляем популярные блюда"""
        with self.connection:
            return self.cursor.execute("INSERT INTO temp_short_menu (`date`, `message_id`,`poll_id`, `ord0`, `ord1`, `ord2`, `ord3`, `ord4`, `ord5`, `ord6`, `ord7`, `ord8`, `ord9`) VALUES(datetime('now', 'localtime'),?,?,?,?,?,?,?,?,?,?,?,?);", (message_id, poll_id, ord0, ord1, ord2, ord3, ord4, ord5, ord6, ord7, ord8, ord9))

    def generate_short_menu(self):
        with self.connection:
            zapros = 'SELECT orders.name, orders.price, orders.order_id, COUNT(*) AS count FROM orders JOIN menu ON orders.order_id = menu.id WHERE menu.active = TRUE GROUP BY orders.order_id ORDER BY count DESC LIMIT 10;'
            return (self.cursor.execute(zapros).fetchall())

    def get_short_menu(self):
        with self.connection:
            zapros = 'SELECT `ord0`, `ord1`, `ord2`, `ord3`, `ord4`, `ord5`, `ord6`, `ord7`, `ord8`, `ord9`, `message_id` FROM `temp_short_menu`;'
            return (self.cursor.execute(zapros).fetchall()[0])

    def empty_short_menu(self):
        with self.connection:
            return self.cursor.execute('DELETE FROM `temp_short_menu`;')

    def del_poll_orders(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `orders` WHERE `user_id` = ? AND `date` = date('now', 'localtime') AND `order_from` = 'poll';", (user_id,))

    def set_user_state(self, user_id, state):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `users` SET `state` = ? WHERE `id` = ?;", (state, user_id))

    def set_active(self, user_id, status):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `users` SET `active` = ? WHERE `id` = ?;", (status, user_id))

    def set_block_menu(self, id, status):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `menu` SET `active` = ? WHERE `id` = ?;", (status, id))

    def set_admin(self, user_id, status):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `users` SET `admin` = ? WHERE `id` = ?;", (status, user_id))

    def set_userdata(self, user_id, given_name, department):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `users` SET `given_name` = ?, `department` = ? WHERE `id` = ?;", (given_name, department, user_id))

    def set_sel_user(self, user_id, sel_user, count):
        with self.connection:
            return self.cursor.execute(
                f"UPDATE `users` SET `selected_user{count}` = ? WHERE `id` = ?;", (sel_user, user_id))

    def empty_selected_users(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `selected_user1` = NULL, `selected_user2` = NULL, `selected_user3` = NULL WHERE `id` = ?;", (user_id,))

    def get_user(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `users` WHERE `id` = ?;', (user_id,)).fetchall()
            if result:
                return result
            else:
                return False

    def get_users_ids(self):
        with self.connection:
            zapros = self.cursor.execute('SELECT `id` FROM users;').fetchall()
            users_ids = []
            for i in zapros:
                users_ids.append(i[0])
            return users_ids

    def get_admins(self):
        with self.connection:
            return self.cursor.execute('SELECT `id` FROM `users` WHERE `admin` = TRUE;').fetchall()

    def get_day_sum(self, user_id, discount):
        with self.connection:
            zapros = self.cursor.execute("SELECT * FROM (SELECT * FROM `orders` WHERE `date` = date('now', 'localtime')) WHERE `order_for_1` = ? OR `order_for_2` = ? OR `order_for_3` = ?;", (user_id, user_id, user_id)).fetchall()
        sum = 0
        for i in zapros:
            s = 0
            for x in [6, 7, 8]:
                if i[x] is not None:
                    s += 1
            sum = sum + i[3] / s
        sum = sum - discount
        if sum > 0:
            return round(sum, 1)
        else:
            return 0

    def get_month_sum(self, user_id, discount):
        with self.connection:
            zapros = self.cursor.execute(f'SELECT SUM([sum_by_one]) FROM (SELECT ([price] / (([order_for_1] IS NOT NULL) + ([order_for_2] IS NOT NULL) + ([order_for_3] IS NOT NULL))) AS "sum_by_one", [date] FROM [orders] WHERE (order_for_1={user_id} OR order_for_2={user_id} OR order_for_3={user_id}) AND ([date] BETWEEN date("now", "start of month", "localtime") AND date("now", "localtime"))) GROUP BY [date];').fetchall()
        sum = 0
        for i in zapros:
            if i[0] > discount:
                sum = sum + i[0] - discount
        return sum

    def get_day_report(self):
        with self.connection:
            return self.cursor.execute("SELECT `user_id`, `date`, `name`, `order_for_1`, `order_for_2`, `order_for_3`, `price` FROM `orders` WHERE `date` = date('now', 'localtime');").fetchall()

    def get_month_report(self, month):
        with self.connection:
            zapros = self.cursor.execute("SELECT `user_id`, `date`, `name`, `order_for_1`, `order_for_2`, `order_for_3`, `price` FROM `orders` WHERE strftime('%m', date) = ? AND strftime('%Y', date) = strftime('%Y', date('now', 'localtime'));", (month,)).fetchall()
            return zapros

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
