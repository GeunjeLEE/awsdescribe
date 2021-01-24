## Local help
### django project start & run app
docker-compose run app django-admin.py startproject pj_awsdescribe . <br>
docker-compose run app python manage.py startapp app_awsdescribe<br>

### make migrate db
docker-compose exec app python manage.py makemigrations app_awsdescribe<br>
### migrate db
docker-compose exec app python manage.py migrate<br>

### create superuser(in this exam, superuser is mediba)
docker-compose exec app python manage.py createsuperuser<br>

### attach shell
docker-compose exec app python manage.py shell<br>
docker-compose exec db python manage.py shell<br>

### collect static files
docker-compose exec app python manage.py collectstatic

### data dump
docker-compose exec app python manage.py dumpdata > dump.json
docker-compose exec app python manage.py loaddata

### login db
docker-compose exec db mysql -u root -p

### run supervisor
docker-compose exec app supervisord -c ./supervisord.conf
