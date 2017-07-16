# Глаза (russian word for eyes)

Глаза stores ansible facts and shows hosts inventories. If you already use ansible, glaza allows you to get automated hosts inventory.

Populating glaza with new facts it's easy, just:

a) Collect facts for a network named stallman.
```
ansible stallman -m setup -u root >tmpfile
```

b) Send facts to rest interface
```
curl -X POST --data-binary "@tmpfile" http://<ip>:8000/rest/
```

Then you can check updated inventory at:
```
http://<ip>:8000/network/Stallman
```

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Glaza its a Django application, that means that you need python. Django's ORM only stores definition of networks (name and network address) so you don't need a big RDBMS. But glaza uses MongoDB for storing ansible's facts.

If you plan to use it on production [Django recomends Apache2 with module WSGI](https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/modwsgi/). 


### Installing

A step by step series of examples that tell you have to get a development env running:

a) Install virtualenv, pip and MongoDB.

```
apt update
apt install virtualenv python3-pip mongodb
```
b) Create a virtualenv and activate it

```
virtualenv --python=`which python3` virtualenv
source virtualenv/bin/activate
```

c) Download the source

```
git clone https://github.com/vcarceler/glaza.git
```

d) Install requirements, make migrations, make admin

```
cd glaza
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

e) Run server

```
python manage.py runserver
```

f) Open your browser, go to /admin and define your networks (name and network address). Don't forget to define a network with address '0.0.0.0' to be able to get a report of all hosts. Populate glaza with facts and that's all!

g) Глаза can check when host's memory changes and send a email notification. If you plan to use this feature don't forget to edit settings.py

```
# Email
# https://sendgrid.com/docs/Integrate/Frameworks/django.html
#
# You need to allow access to less secure applications (gmail account settings)

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'glaza@elpuig.xeill.net'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 587

# EMAIL notifications
#
EMAIL_RECIPIENT_LIST = [
    'incidencies@elpuig.xeill.net',
]
```

## Built With

* [Django](https://www.djangoproject.com/) - Web framework
* [MongoDB](https://www.mongodb.com/) - NoSQL database
* [Python](https://www.python.org/) - Programming language
* [Bootstrap](http://getbootstrap.com/) - Front-end web framework

## Authors

* **Victor Carceler**

## License

This project is licensed under the GNU General Public License v3.0 - see the [COPYING](COPYING) file for details.
