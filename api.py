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

from flasgger import Swagger

es = Elasticsearch()
api = Flask(__name__)
swagger = Swagger(api)

# ---------------------------------------------------------------------------------------
# endpoints

@api.route('/distinct/<field>')
def field_values(field):
    """returns a list of possible values for a given field
    do a distinct on provided field
    ---
    parameters:
      - name: field
        in: path
        type: string
        enum: ['prices_merchant', 'brand', 'manufacturer']
        required: true
    responses:
      404:
        description: ressource not found
      200:
        description: OK
    """
    if field in ('prices_merchant', 'brand', 'manufacturer'):
      body = {
          "size": 0,
          "aggs": {
             "field_values": {
                "terms": {
                  "field": field+".keyword"
                }
             }
          }
      }
    else:
      abort(400)

    res = es.search(index="electronics_products", body=body, size=100)
    return jsonify(res["aggregations"])

@api.route('/status')
def return_status():
    """returns the API status
    just return ES status to prove the API is reachable
    ---
    responses:
      200:
        description: OK
    """
    results = es.info()
    return jsonify(results)

@api.route('/search')
def search_entries():
    """do a research on specific fields
    do a research on specific fields
    ---
    parameters:
      - name: brand
        in: query
        type: string
      - name: manufacturer
        in: query
        type: string
    responses:
      404:
        description: ressource not found
      200:
        description: OK
    """
    brand = request.args.get('brand')
    manufacturer = request.args.get('manufacturer')

    if brand and manufacturer:
      abort(400)

    elif brand:
      body = {
          "query": {
              "match": {
                  "brand": brand
              }
          }
      }

    elif manufacturer:
      body = {
          "query": {
              "match": {
                  "manufacturer": manufacturer
              }
          }
      }

    else:
      abort(400)

    res = es.search(index="electronics_products", body=body, size=100)

    return jsonify(res['hits']['hits'])

# ---------------------------------------------------------------------------------------
# exceptions

@api.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)

@api.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

# ---------------------------------------------------------------------------------------
# main

if __name__ == '__main__':
    api.run(host="0.0.0.0", port=5000)


