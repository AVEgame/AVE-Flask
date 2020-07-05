# AVE-Flask
A flask based website for AVE, designed to replace the js version.

## Deployment
To deploy this website, clone the repo with

```
git clone --recurse submodules https://github.com/AVEgame/AVE-Flask
```

Install requirements with

```
pip install -r requirements.txt
```

### Testing

You can test the server locally by running:

```
FLASK_APP=app.py # only needs to be run once
FLASK_ENV=development # add to run in debug mode
flask run
```

## WSGI server

You will need to run a WSGI server, probably behind a reverse proxy to serve content in a production environment, an example systemd file for gunicorn is included.