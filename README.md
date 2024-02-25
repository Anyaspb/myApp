MyApp
Приложение для заказа продуктов

Установка:
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver

Загрузка данных:
loaddata fixures/db_Caterogy.json
loaddata fixures/db_Product.json
loaddata fixures/db_Supplier.json
loaddata fixures/db_User.json

Тестинг Postman реквесты:
https://documenter.getpostman.com/view/32288026/2sA2rDvLEq

В проекте MyApp 3 приложения:
- Users (авторизация, регистрация настроены через Frontend)
- Suppliers (каталог товаров)
- Clients (заказы)
  




