# Farm Management
A tool to manage a farm
## Install
### Application, virtual environment and requirements
Clone the folder, go inside, create a virtual environment for Python with virtualenv (*!!! maybe you have to install [virtualenv](https://virtualenv.pypa.io/en/stable/) !!!*), activate it and install all necessary dependencies ([django](https://www.djangoproject.com/foundation/), [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/en/stable/)):
```shell
$ git clone https://github.com/JBthePenguin/Projet.git
$ cd Projet
$ virtualenv -p python3 env
$ source env/bin/activate
(env)$ pip install -r requirements.txt
```
### Tables
Make the migrations:
```shell
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
```
### Admin site
Create a "superuser" account:
```shell
(env)$ python manage.py createsuperuser
```
## Using
Start the server:
```shell
(env)$ python manage.py runserver
```
**NOW, with your favorite browser, go to this url [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to use the application and [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin) for the admin site.**
