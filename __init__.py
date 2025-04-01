from flask import Flask, render_template, jsonify, json
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
    try:
        response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
        results = []
        for list_element in json_content.get('list', []):
            dt_value = list_element.get('dt')
            temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin en °C 
            results.append({'Jour': dt_value, 'temp': temp_day_value})
        return jsonify(results=results)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def exercice4():
    return render_template("histogramme.html")

def extract_minutes(date_string):
    """
    Extrait la minute à partir d'une date au format ISO 8601 (ex: "2024-02-11T11:57:27Z").
    """
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    return date_object.minute

@app.route('/commits/')
def commits_page():
    try:
        # Appel à l'API GitHub via urlopen
        response = urlopen("https://api.github.com/repos/OpenRSI/OpenRSI/Exo_Java_BDD_2023")
        raw_data = response.read()
        commits_data = json.loads(raw_data.decode('utf-8'))
        
        # Agrégation des commits par minute
        commit_minutes = {}
        for commit in commits_data:
            # Vérifier que la clé existe bien
            date_str = commit.get('commit', {}).get('author', {}).get('date')
            if date_str:
                minute = extract_minutes(date_str)
                commit_minutes[minute] = commit_minutes.get(minute, 0) + 1
        
        # Préparation des données pour le graphique : liste de paires [minute, nombre_de_commits]
        graph_data = sorted([[minute, count] for minute, count in commit_minutes.items()], key=lambda x: x[0])
        
        # Passage des données au template commits.html
        return render_template('commits.html', data=graph_data)
    except Exception as e:
        # Retourne l'erreur pour déboguer
        return f"Erreur lors du traitement des commits : {e}", 500

if __name__ == "__main__":
    app.run(debug=True)
