# SGRED
Sistema de Gestión de Recursos Educativos Digitales

[ ![Codeship Status for haortizr/SGRED](https://app.codeship.com/projects/7dfb9be0-9c75-0136-4044-122b2fcde96f/status?branch=master)](https://app.codeship.com/projects/305830)
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/070dab54606b413e97fd86ab9711a66a)](https://www.codacy.com/app/NestorRomeroUAndes/SGRED?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=haortizr/SGRED&amp;utm_campaign=Badge_Grade)
## Prerequisitos
* Install python2.7, install pip, install git
## Como Ejecutar 
* Clone this repo on your local device using *git clone https://github.com/haortizr/SGRED.git*

Follow the next command line expressions for the initial configuration on linux systems, commands may vary depending on your operating system

* cd AgileDjango
* pip install virtualenv
* cd gallery
#En linux/unix
* virtualenv -p /usr/bin/python2.7 env
#En Windows
virtualenv -p C:\Python27\python.exe env
* cd env
* source bin/activate
* pip install django
* pip install psycopg2
* pip install whitenoise
* pip install gunicorn
* pip install Pillow
* cd ../..
* python manage.py runserver

Now the server is runing at 
http://127.0.0.1:8000/admin


No subir archivos de migraciones, solo se subiran los modelos y cada persona realizará la migración, al final una persona realizará la ejecución de las migraciones en la base de datos de producción. Seguir los siguientes pasos.

Después de descargar cambios

1. Descargar los cambios
2. Borrar la BD por el manejador de base de datos
3. Crear el esquema otra vez a través del manejador de base de datos
4. python manage.py makemigrations (en la terminal de pycharm)
5. python manage.py migrate
6. Crear el super usuario python manage.py createsuperuser




