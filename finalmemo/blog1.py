# 17:50
import math
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)
boards_col = client.dbsparta.boards

@app.route('/')
def home():
    return render_template('blog1.html') # 조심

@app.route('/memo', methods=['POST'])
def post_article():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    article = {
        'title': title_receive
        , 'content': content_receive
        }

    boards_col.insert_one(article)

    return jsonify({'result': 'success'})

@app.route('/memo', methods=['GET'])
def read_articles():
    page_receive = request.args.get('page_give', 1, type=int) #
    limit = 5
    search_receive = request.args.get('search_give', -1, type=int)
    keyword_receive = request.args.get('keyword_give', "", type=str)
    
    query = {}
    searches = []
    
    if search_receive == 0:
        searches.append({'title': {"$regex": keyword_receive}})
        searches.append({'content': {"$regex": keyword_receive}})
    elif search_receive == 1:
        searches.append({'title': {"$regex": keyword_receive}})
    elif search_receive == 2:
        searches.append({'content': {"$regex": keyword_receive}})
    elif search_receive == 3:
        searches.append({'name': {"$regex": keyword_receive}})
        
    if len(searches) > 0:
        query['$or'] = searches
    
    results = list(boards_col.find(query).sort('regdate', -1).skip((page_receive - 1)*limit).limit(limit))

    total_cnt = boards_col.count_documents(query)
    last_page = math.ceil(total_cnt / limit) #
    
    block_size = 5
    current_block = math.ceil(page_receive / block_size)
    last_block = math.ceil(last_page / block_size)
    
    block_first = (current_block - 1) * block_size + 1 #
    block_last = block_first + block_size - 1 #
    
    if current_block == last_block:
        block_last = last_page

    print(page_receive, last_page, block_first, block_last)
    # 페이지네이션 끝
    
    articles = []
    for result in results:
        article = {
            '_id': str(result['_id'])
            , 'title': result['title']
            , 'content': result['content']
        }
        articles.append(article)
        
    return jsonify({
        'result': 'success'
        , 'articles': articles
        , 'page': page_receive
        , 'last_page': last_page
        , 'block_first': block_first
        , 'block_last': block_last
        })

@app.route('/memo/<_id>', methods=['PATCH'])
def update_article(_id):
    _id_receive = ObjectId(_id)
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    article = {
        'title': title_receive
        , 'content': content_receive
        }

    boards_col.update_one({'_id': _id_receive}, {'$set' : article})

    return jsonify({'result': 'success'})

@app.route('/memo/<_id>', methods=['DELETE'])
def delete_article(_id):
    _id_receive = ObjectId(_id)

    boards_col.delete_one({'_id': _id_receive})

    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)