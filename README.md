Installation instructions for Windows
Create virtual environment
python3 -m venv env

Activate environment
env/scripts/activate



create tables using migrations
python manage.py makemigrations

python manage.py migrate

start server locally
python manage.py runserver

Api URLs
 for admin page 'http://127.0.0.1:8000/admin/' 
for signin (post)  'http://127.0.0.1:8000/signin/'
for login (get) 'http://127.0.0.1:8000/'login/'

for logout (post)  'http://127.0.0.1:8000/logout/'  
for offer_details(crud) 'http://127.0.0.1:8000/offer-details',
End points:
    user_id (integer field)
    username(char field)
    email(email field)
    password(char field)
