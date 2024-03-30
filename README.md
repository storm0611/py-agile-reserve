# AgileReserveSys
This website for booking local computer to use it remotely to the customers
## Pre Requirements
You need to have local networks of computers that can be booked.
Ip range can be 192.168.x.x, and can be configured.
Then you need to install python 3.x.x
## Run the project
### Install necessary packages
```cli
pip install -r requirements.txt
```
### Generating a local SSL certificate
Check this link: https://timonweb.com/django/https-django-development-server-ssl-certificate/
### Run the Server with Https
```cli
python manage.py runserver_plus --cert-file cert.pem --key-file key.pem
```
Server will running on https://localhost:8000
