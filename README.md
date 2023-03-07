# SWAPI Collector

SWAPI Collector is a Django application for collecting and inspecting information about Star Wars characters.
It fetches the data from [SWAPI](https://swapi.dev/).

## Installation
Clone yourself a local version of the application.
```bash
git clone https://github.com/d-szuffy/django-swapi.git .
```

Next, in the root directory of the project create virtual environment and activate it.

```bash
python3 -m venv env
source env/bin/activate
```

If successful, now you should see **(env)** in the beginning of each line in your terminal session.
Once you activated your **env** you can install project's requirements.

```bash
pip install -r requirements.txt
```

Run database migrations, collect static files and create media files directory.
```bash
python manage.py makemigrations datacollections
python manage.py migrate
python manage.py collectstatic
mkdir datacollections/media
```

And finally, you can run the application server.
```bash
python manage.py runserver
```

Visit your app at [http://localhost:8000](http://localhost:8000)
