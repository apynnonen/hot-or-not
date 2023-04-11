# hot-or-not

The only required tools to run this program are flask, selenium and vaderSentiment.
Both can be installed with pip install, but more installation details can be found in the links below

Flask installation:
https://flask.palletsprojects.com/en/2.2.x/installation/

Selenium installation:
https://selenium-python.readthedocs.io/installation.html

VADER Sentiment installation:
https://pypi.org/project/vaderSentiment/

Once the required tools are installed, this program can be ran using the following command:
flask --app app --debug run --host 0.0.0.0 --port 8000
Then visit http://127.0.0.1:8000 to see the website up

If you want to be able to step through and actually debug the program, use the launch.json file I've added to github. It'll then hit your breakpoints.

The actual website requires a professor's name and university to be inputted into the respective fields as well as a proper option to be selected. The program may take up to 30 seconds or more but will retrieve and store professor information for much faster loads of professors who have already been searched for in a given session. The website also calculates all methods which allows the user to quickly load the results to alternative methods upon switching their option and running the program again.
