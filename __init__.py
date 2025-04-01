import requests
from datetime import datetime
from flask import Flask, jsonify, render_template
                                                                                                         
app = Flask(__name__)    

def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    return date_object.minute
                                                                                                                                       
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
def commits():
    # Appel à l'API GitHub
    response = requests.get("https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits")
    commit_data = response.json()

    # Agrégation des commits par minute
    commit_minutes = {}
    for commit in commit_data:
        date_str = commit['commit']['author']['date']
        minute = extract_minutes(date_str)
        commit_minutes[minute] = commit_minutes.get(minute, 0) + 1

    # Préparation des données pour le graphique
    # On crée une liste de listes : [[minute, nombre_de_commits], ...]
    graph_data = sorted([[minute, count] for minute, count in commit_minutes.items()], key=lambda x: x[0])

    # Optionnel : Si tu préfères renvoyer les données au format JSON, tu peux le faire directement
    # return jsonify(commits=graph_data)

    # Sinon, passe les données à un template HTML pour générer le graphique
    return render_template("commits.html", data=graph_data)
  
if __name__ == "__main__":
  app.run(debug=True)
  
