from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/contact')
def exercice2():
    return render_template('contact.html')


@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def exercice4():
    return render_template("histogramme.html")

@app.route('/commits/')
def commits_page():
    return render_template('commits.html')

import requests
from datetime import datetime
from flask import jsonify

@app.route('/api/commits-data/')
def commits_data():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits = response.json()

    commit_minutes = {}

    for commit in commits:
        try:
            date_str = commit['commit']['author']['date']
            dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minute = dt.minute
            commit_minutes[minute] = commit_minutes.get(minute, 0) + 1
        except Exception as e:
            print("Erreur de parsing :", e)

    return jsonify(commit_minutes)

  
if __name__ == "__main__":
  app.run(debug=True)
  
