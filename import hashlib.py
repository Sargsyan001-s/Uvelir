import sys

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cart = set()  # Корзина (множество)
        self.purchase_history = []  # История покупок (список)

    def add_to_cart(self, item):
        self.cart.add(item)

    def purchase(self):
        self.purchase_history.extend(self.cart)
        self.cart.clear()

    def view_cart(self):
        if self.cart:
            return list(self.cart)  # Возвращаем товары в виде списка
        else:
            return "Корзина пуста."

    def view_purchase_history(self):
        return self.purchase_history

    def clear_cart(self):
        self.cart.clear()

    def update_password(self, new_password):
        self.password = new_password
        
        
    def format_items(self, items): # Функция форматирования вывода
        if not items:
            return "Товары не найдены."
        result = "{:<5} {:<25} {:<10}\n".format("ID", "Название", "Цена")
        for item in items:
            result += "{:<5} {:<25} {:<10}\n".format(item['id'], item['name'], item['price'])
        return result 
        
class Admin(User): # Предполагается, что у вас уже есть класс User
    def __init__(self, username, password):
        super().__init__(username, password) # Вызов инициализатора родительского класса
        self.items = [
            {'name': 'Кольцо с бриллиантом', 'price': 35000, 'id': 1},
            {'name': 'Кольцо с фианитом', 'price': 20000, 'id': 2},
            {'name': 'Золотые серьги', 'price': 6780, 'id': 3},
            {'name': 'Серебряные серьги', 'price': 1500, 'id': 4},
            {'name': 'Колье золотое', 'price': 8000, 'id': 5},
            {'name': 'Колье серебряное', 'price': 4500, 'id': 6}
        ]

    def add_item(self, item_name, price):
        new_id = max(item['id'] for item in self.items) + 1 if self.items else 1
        self.items.append({'name': item_name, 'price': price, 'id': new_id})

    def remove_item(self, item_id):
        self.items = [item for item in self.items if item['id'] != item_id]

    def view_items(self, sort_by=None, filter_price=None):
        items_to_show = self.items[:] # Создаем копию, чтобы не менять оригинал

        if filter_price:
            items_to_show = [item for item in items_to_show if item['price'] <= filter_price]

        if sort_by:
            items_to_show.sort(key=lambda x: x[sort_by], reverse=True)

        if not items_to_show:
            print("Изделия не найдены.")
            return

        print("{:<5} {:<25} {:<10}".format("ID", "Название", "Цена"))
        for item in items_to_show:
            print("{:<5} {:<25} {:<10}".format(item['id'], item['name'], item['price']))


    def filter_items_by_price(self, max_price):
        filtered_items = [item for item in self.items if item['price'] <= max_price]
        return self.format_items(filtered_items) # Возвращаем отформатированную строку

    def sort_items_by_price(self):
        sorted_items = sorted(self.items, key=lambda x: x['price'])
        return self.format_items(sorted_items)


def user_menu(user, admin): # admin добавлен как аргумент
    while True:
        print("1. Просмотреть товары")
        print("2. Добавить товар в корзину")
        print("3. Посмотреть корзину")
        print("4. Купить товары из корзины")
        print("5. Просмотреть историю покупок")
        print("6. Изменить пароль")
        print("7. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            print(admin.view_items())
        elif choice == "2":
            item_id = input("Введите ID товара для добавления в корзину: ")
            try:
                item_id = int(item_id)
                item = next((item for item in admin.items if item['id'] == item_id), None)
                if item:
                    user.add_to_cart(item)
                    print(f"Товар добавлен в корзину: {item['name']}")
                else:
                    print("Товар не найден.")
            except ValueError:
                print("Неверный формат ID.")
        elif choice == "3":
            print(user.view_cart())
        elif choice == "4":
            user.purchase()
            print("Товары успешно куплены.")
        elif choice == "5":
            print(user.view_purchase_history())
        elif choice == "6":
            new_password = input("Введите новый пароль: ")
            user.update_password(new_password)
            print("Пароль обновлён.")
        elif choice == "7":
            break

def admin_menu(admin):
    while True:
        print("1. Добавить товар")
        print("2. Удалить товар")
        print("3. Просмотреть товары")
        print("4. Фильтровать товары по цене")
        print("5. Сортировать товары по цене")
        print("6. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            item = input("Введите название товара: ")
            price = float(input("Введите цену товара: "))
            admin.add_item(item, price)
            print(f"Товар добавлен: {item} по цене {price}")
        elif choice == "2":
            item = input("Введите название товара для удаления: ")
            admin.remove_item(item)
            print(f"Товар удален: {item}")
        elif choice == "3":
            print(admin.view_items())
        elif choice == "4":
            max_price = float(input("Введите максимальную цену: "))
            print(admin.filter_items_by_price(max_price))
        elif choice == "5":
            print(admin.sort_items_by_price())
        elif choice == "6":

            break

# Основная программа
admin = Admin("admin", "admin_password")

username = None
password = None

while True:
    print("1. Войти как пользователь")
    print("2. Войти как администратор")
    print("3. Выйти")
    role = input("Выберите роль: ")

    if role == "1":
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        user = User(username, password)
        user_menu(user, admin) # admin передается в user_menu

    elif role == "2":
        admin_username = input("Введите логин администратора: ")
        admin_password = input("Введите пароль администратора: ")

        if admin_username == "admin" and admin_password == "admin_password":
            admin_menu(admin)
        else:
            print("Неверные учетные данные!")

    elif role == "3":
        sys.exit()