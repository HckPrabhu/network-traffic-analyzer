from flask import Flask, render_template, jsonify
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/data')
def get_data():
    conn = sqlite3.connect('../../database/traffic.db')
    df = pd.read_sql('SELECT * FROM traffic', conn)
    
    traffic_by_ip = df.groupby('src_ip').size().nlargest(10)
    protocols = df['protocol'].value_counts()
    
    plt.figure(figsize=(10, 5))
    traffic_by_ip.plot(kind='bar')
    plt.title('Top 10 Source IPs by Traffic Volume')
    plt.ylabel('Packets')
    plt.xlabel('IP Address')
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return jsonify({
        'top_ips': traffic_by_ip.to_dict(),
        'protocols': protocols.to_dict(),
        'plot': f"data:image/png;base64,{plot_url}"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
