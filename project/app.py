from flask import Flask, render_template, jsonify, request, url_for
import pandas as pd
from pymongo import MongoClient

import matplotlib.pyplot as plt

app = Flask(__name__)
client = MongoClient('localhost', 27017)

@app.route('/')
def home() :
    return render_template('index.html')

@app.route('/scatterplot', methods=['GET'])
def scatterplot_home():
    return render_template('scatterplot_index.html')

df = pd.DataFrame()
@app.route('/scatterplot', methods=['POST'])
def draw_scatterplot() :
    data = request.form['data_give']
    rows = data.split('\n')
    Frame = []
    for row in rows:
        row = row.split('\t')
        Frame.append(row)
    global df

    df = pd.DataFrame(Frame, columns=Frame[0])
    df.dropna(axis=0, inplace=True)
    df = df.loc[1:]

    return jsonify({'result' : 'success', 'msg' : '데이터 입력 완료'})

@app.route('/scatterplot/getcolumns', methods=['GET'])
def send_columns():
    global df
    columns = list(df.columns)
    return jsonify({'result': 'success', 'columns': columns})

@app.route('/scatterplot/InputAttribute', methods=['POST'])
def draw_chart() :
    global df
    x_axis, y_axis, title, color = request.form['x_axis_give'], request.form['y_axis_give'], request.form['title_give'], request.form['color_give']

    df.plot(
        kind='scatter',
        x = x_axis,
        y = y_axis,
        c=  color,
    )


    plt.title(title)
    plt.savefig('templates/static/image/plot.png')
    return jsonify({'result': 'success', 'msg': '그래프 그리기 완료'})


@app.route('/scatterplot/InputAttribute', methods=['GET'])
def send_chart() :
    img_tag = "static/image/plot.png"
    return jsonify({'img_tag': img_tag})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
