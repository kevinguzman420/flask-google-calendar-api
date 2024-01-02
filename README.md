# Python - Google Calendar API

## Get and create events with Google Calendar API using Flask for the API

### Use this code

1. Create a virtual environment:
   `python3 -m venv venv`
2. Create the APP_SETTINGS_MODULE var env (use to configure the app env)
   `export APP_SETTINGS_MODULE=config.dev` set this in you Linux terminal.
3. Activate the virtual environment
   `source venv/bin/activate`
4. Install the requirements project:
   `pip install -r requirements.txt`
5. Start the Flask server:
   `flask --app entrypoint.py run`
6. Make request GET & POST to `http://localhost:5000`


Remember configure Google Console to get permissions before to can use this API:
[Google Calendar API](https://developers.google.com/calendar/api/quickstart/python)
