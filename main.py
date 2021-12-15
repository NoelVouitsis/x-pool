import pandas as pd
import os
from flask import Flask, render_template, request, g, Response
from random import randrange, randint
import numpy as np
import plotly.graph_objs as go
import plotly.offline as plt
import json
import plotly
import plotly.express as px

app = Flask(__name__)
df = pd.read_csv('static/MSRVTT_JSFUSION_test.csv')
total_vids = len(df)
attn_weights = np.load('attn_weights.npy')
v_num = 0

data = {'title': 'Chart'}

@app.route("/data")
def chart_data():
    data_set = [i.item() for i in attn_weights[v_num, :]]
    data = {'set': data_set}
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

def get_random_vid():
    global v_num
    v_num = randrange(total_vids)
    vid = os.path.join('videos', df.iloc[v_num].video_id + '.mp4')
    caption = df.iloc[v_num].sentence
    return vid, caption

@app.route('/', methods=['POST', 'GET'])
def handle():
    if request.method == 'POST':
        if request.form.get('Generate') == 'Generate':
            vid, caption = get_random_vid()
            return render_template('index.html', vid=vid, caption=caption, data=data)
        else:
            vid, caption = get_random_vid()
            return render_template('index.html', vid=vid, caption=caption, data=data)
    else:
            vid, caption = get_random_vid()
            return render_template('index.html', vid=vid, caption=caption, data=data)


if __name__ == '__main__':
    app.run(debug=True)
