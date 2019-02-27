# Hospitality Club 4.0 Open Source - Django

## Environment Assumptions

Assuming developing in Debian/Ubuntu family Linux distribution.
Required system dependencies: 

* `python3` (3.6)
* `postgresql-10` (10.6)
* `node` and `npm`

## Development setup

* Git clone
* Create virtual environment and activate it
```bash
virtualenv -p python3 ./venv
source ./venv/bin/activate
```
* Install dependencies
```bash
pip -r ./dependencies/py3.txt
```
* Install node modules
```bash
cd cointelligence/node_modules
npm install
cd ../..
```
* Update git submodules
```bash
git submodule update --remote --recursive --init
```
* Create Postgres role (user) and database owned by the role, we recommend using PgAdmin3
* Update `hc4/settings.py` DATABASES constant
* From now we work in hc4 project directory
```bash
cd hc4
```
* Run migrations
```bash
python manage.py migrate
```
* Create superuser
```bash
python manage.py createsuperuser
```
* Populate Cities/Regions/Countries (takes forever)
```bash
python manage.py cities_light
```
* Run debug server
```bash
python manage.py runserver
```
It should start working on localhost:8000

Happy testing and development!
