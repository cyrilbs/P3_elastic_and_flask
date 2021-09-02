from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request, abort

import pandas as pd
import random
import sys
import json

from elasticsearch import Elasticsearch

es = Elasticsearch()
api = Flask(__name__)

# ---------------------------------------------------------------------------------------
# endpoints

@api.route('/status', methods=['GET'])
def return_status():
     #results = es.get(index='electronics_products', doc_type='_doc', id='tmQEqHsBtnz6c2wlEgfw')
     #return jsonify(results['_source'])
     results = es.info()
     return jsonify(results)
 
     #doc = {
     # 'author': 'kimchy',
     # 'text': 'Elasticsearch: cool. bonsai cool.',
     # 'timestamp': datetime.now(),
     #}
     #results = es.index(index="electronics_products", id=1, body=doc)
     #return jsonify(results)

@api.route('/search', methods=['GET'])
def doc():
    brand = request.args.get('brand')
    body = {
        "query": {
            "match": {
                "brand": brand
            }
        }
    }

    res = es.search(index="electronics_products", body=body)

    return jsonify(res['hits'])


# ---------------------------------------------------------------------------------------
# exceptions

@api.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)

@api.errorhandler(403)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Not authorized'}), 403)

@api.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

# ---------------------------------------------------------------------------------------
# main

if __name__ == '__main__':
    api.run(host="0.0.0.0", port=5000)


