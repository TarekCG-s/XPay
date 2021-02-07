# XPAY Task

The Web part of XShop's system.

## Steps

- Install Python 3.8
- pip3 install -r requirements.txt
- python3 manage.py makemigrations
- python3 manage.py migrate
- python3 manage.py create_staff_user
- python3 manage.py test
- python3 manage.py generate_small_data
- Import XPay Postman collection. 
- Invoke Answers request. Default username=admin, password=admin .
- python3 manage.py remove_all_data
- python3 manage.py generate_large_data
