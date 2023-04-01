import script
import flask
import json
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/test', methods=['POST', 'GET'])
def show_homepage():
    context = {
        'result': ''
    }
    if flask.request.method == 'POST':
        output = flask.request.get_json()
        print(output)
        y = script.call(output["name"], output["uni"], output["op"])
        print(y)
        x = {"answer": y}
        # x['answer'] += y
        print(x)
        return x
        # User has attempted to search for a professor, lets give 'em what they need
        # form = flask.request.form
        # summary = script.call(form.get('Professor Name'), form.get(
        #     'University'), form.get('sentiment_choice'))
        # context['result'] = summary


if __name__ == "__main__":
    app.run(debug=True)
