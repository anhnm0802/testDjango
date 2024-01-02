Vào được đường dẫn của tệp voting_system

Trước tiên cần tạo môi trường ảo env thông qua virtualenv bằng lệnh 
virtualenv env

Bật môi trường ảo bằng lệnh
source env/bin/activate

Sau đó cài các gói có sẵn trong file requirements.txt thông qua các lệnh
pip install django
pip install psycopg2-binary
pip install requests
pip install twilio
pip install djangorestframework
python -m pip install Pillow


Chạy thử chương trình bằng 
python manage.py runserver 
rồi đi theo đường dẫn là
http://127.0.0.1:8000/account/login/# 

Giao diện được thiết kế bằng tiếng việt nên người dùng có thể sử dụng một cách dễ dàng
# django_DATN
# django_DATN
