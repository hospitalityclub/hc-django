# Hospitality Club 4.0 Open Source - Django

## Environment Assumptions

Assuming developing in Debian/Ubuntu family Linux distribution.
Required system dependencies: 

* `python3` (3.6)
* `postgresql-10` (10.6)
* `node` and `npm`

## Development setup

1. Git clone
2. Create virtual environment and activate it
```
virtualenv -p python3 ./venv
source ./venv/bin/activate
```
3. Install dependencies
```
pip ./dependencies/py3.txt
```
4. Install node modules
```
cd cointelligence/node_modules
npm install
cd ../..
```
5. Update git submodules
```
git submodule update --remote --recursive --init
```
6. Create Postgres role (user) and database owned by the role, we recommend using PgAdmin3
7. Update `hc4/settings.py` DATABASES constant
8. From now we work in hc4 project directory
```
cd hc4
```
9. Run migrations
```
python manage.py migrate
```
10. Create superuser
```
python manage.py createsuperuser
```
11. Run debug server
```
python manage.py runserver
```
It should start working on localhost:8000

Happy testing and development!
