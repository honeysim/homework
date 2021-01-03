from flask import Flask, render_template, jsonify, request
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def home() :
    return render_template('scatterplot_index.html')

@app.route('/scatterplot', methods=['POST'])
def draw_scatterplot() :
    data = request.form['data_give']
    data = data.split('\n')
    list = []
    for i in data:
        row = i.split('\t')
        list.append(row)
    df = pd.DataFrame(list, columns=list[0])
    df = df.loc[1:]
    df.plot(kind='scatter', x='weight', y='mpg', c='coral', s=10, figsize=(10, 5))
    plt.title('Scatter Plot - mpg vs. weight')
    plt.savefig('savefig_default2.png')
    return jsonify({'result': 'success'})
# 일단 여기까지~
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
