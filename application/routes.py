#from application import app
from flask import current_app as app
from flask import render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import os

global path_file,path_file_json
path_file = os.path.join(os.path.dirname(__file__), './data/', 'file.csv')
path_file_json = os.path.join(os.path.dirname(__file__), '../', 'data.json')

@app.route('/')
def index():    
    return render_template('index.jinja2')



@app.route('/apriori/')
def apriori():
    print(path_file)
    df = pd.read_csv(path_file) 
    data = df.to_dict(orient='records')
    return render_template('layout_Apriori.jinja2', title="Apriori", data=data)

@app.route('/clustering/')
def clustering():
    # Agregar la llamada a métodos de cada algoritmo
    return render_template('layout_Clustering.jinja2',
            title="Clustering")

@app.route('/metricas/')
def metricas():
    # Agregar la llamada a métodos de cada algoritmo
    return render_template('layout_Metricas.jinja2',
            title="Metricas")

# Decorador de carga para la carga y sobreescritura de los archivos
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'csv_file' not in request.files:
        return "No file uploaded"
    
    file = request.files['csv_file']
    
    if file.filename == '':
        return "No file selected"
    
    if file and file.filename.endswith('.csv'):
        csv_data = pd.read_csv(file)
        csv_data.to_csv(os.path.join(app.root_path, 'data/file.csv'), index=False)
        return "CSV file uploaded successfully and overwritten data.csv"
    else:
        return "Invalid file format. Please upload a CSV file."


## Ejemplo de cierta ruta
@app.route('/chart1')
def chart1():

    # Graph One
    df = px.data.medals_wide()
    fig1 = px.bar(df, x="nation", y=["gold", "silver", "bronze"], title="Wide-Form Input")
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph two
    df = px.data.iris()
    fig2 = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
              color='species',  title="Iris Dataset")
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph three
    df = px.data.gapminder().query("continent=='Oceania'")
    fig3 = px.line(df, x="year", y="lifeExp", color='country',  title="Life Expectancy")
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)


    return render_template('index.html', graph1JSON=graph1JSON,  graph2JSON=graph2JSON, graph3JSON=graph3JSON)

