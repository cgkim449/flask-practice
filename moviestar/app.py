from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbjungle

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/list', methods=['GET'])
def show_stars():
    stars = list(db.mystar.find({}, {'_id': False}).sort('like', -1))
    return jsonify({'result': 'success', 'stars_list': stars})

@app.route('/api/like', methods=['POST'])
def like_star():
    name_receive = request.form['name_give']

    star = db.mystar.find_one({'name': name_receive})
    new_like = star['like'] + 1

    db.mystar.update_one({'name': name_receive}, {'$set': {'like': new_like}})

    return jsonify({'result': 'success'})

@app.route('/api/delete', methods=['POST'])
def delete_star():
    name_receive = request.form['name_give']
    db.mystar.delete_one({'name': name_receive})
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)