from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('localhost',27017)

db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/memo', methods=['POST'])
def post_article():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    article = {
        'title': title_receive
        , 'content': content_receive
        }

    db.articles.insert_one(article)

    return jsonify({'result': 'success'})

@app.route('/memo', methods=['GET'])
def read_articles():
    results = list(db.articles.find({}))
    
    articles = []
    for result in results:
        article = {
            '_id': str(result['_id'])
            , 'title': result['title']
            , 'content': result['content']
        }
        articles.append(article)
        
    return jsonify({'result': 'success', 'articles': articles})

@app.route('/memo/<_id>', methods=['PATCH'])
def update_article(_id):
    _id_receive = ObjectId(_id)
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    article = {
        'title': title_receive
        , 'content': content_receive
        }

    db.articles.update_one({'_id': _id_receive}, {'$set' : article})

    return jsonify({'result': 'success'})

@app.route('/memo/<_id>', methods=['DELETE'])
def delete_article(_id):
    _id_receive = ObjectId(_id)

    db.articles.delete_one({'_id': _id_receive})

    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)