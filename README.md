
## как запустить

1. cd furniture_shop
2. создайте env
3. python -m venv venv -создание виртуального окружения если его нет
4. venv\Scripts\activate  -активация виртуального окружения
5. pip install -r requirements.txt  -устновка зависимостей
6. mysql -u root -p < database_schema.sql  -создание бд
7. python manage.py makemigrations 
8. python manage.py migrate -выполение миграций
9. python manage.py seed -заполнение бд
10. python manage.py createsuperuser  -создание админа
11. python manage.py runserver  -заппуск

12. или откройте  https://maintenance-wonderful-journey-cheese.trycloudflare.com/


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

=======
# courseWork_ISiP-42321

