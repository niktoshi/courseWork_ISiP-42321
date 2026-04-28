## как запустить

1. cd furniture_shop
2. python -m venv venv -создание виртуального окружения если его нет
3. venv\Scripts\activate  -активация виртуального окружения
4. pip install -r requirements.txt  -устновка зависимостей
5. mysql -u root -p < database_schema.sql  -создание бд
6. python manage.py makemigrations 
7. python manage.py migrate -выполение миграций
8. python manage.py seed -заполнение бд
9. python manage.py createsuperuser  -создание админа
10. python manage.py runserver  -заппуск


## Основные страницы
- `/` — главная
- `/catalog/` — каталог
- `/product/<slug>/` — карточка товара
- `/cart/` — корзина
- `/orders/` — список заказов пользователя
- `/orders/checkout/` — оформление заказа
- `/orders/detail/<id>/` — детали заказа
- `/users/login/` — вход
- `/users/register/` — регистрация
- `/users/profile/` — профиль
- `/admin/` — административная панель

## Технологии

- Django
- MySQL
- mysqlclient
- Pillow
- python-dotenv

