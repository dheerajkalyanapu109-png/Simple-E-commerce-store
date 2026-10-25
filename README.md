# Fernwick — Django e-commerce demo
    pip install -r requirements.txt
    python manage.py makemigrations shop
    python manage.py migrate
    python manage.py seed              # sample products
    python manage.py createsuperuser   # for /admin/ (manage products and orders)
    python manage.py runserver         # http://127.0.0.1:8000
