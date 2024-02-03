"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def add_member():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg':'Debes enviar inf en el body'})
    if 'first_name' not in body:
        return ({'msg':'El campo name es requerido'})
    if 'age' not in body:
        return ({'msg':'El campo age es requerido'})
    if 'lucky_numbers' not in body:
        return ({'msg':'El campo lucky_numbers es requerido'})
    if 'id' in body:
        id_member = body['id']
    else:
        # Generar un id aleatorio si no se proporciona
        id_member = jackson_family._generateId()

    new_member = {
        'id': id_member,
        'first_name': body['first_name'],
        'last_name': jackson_family.last_name,
        'age': body['age'],
        'lucky_numbers': body['lucky_numbers']
    }

    jackson_family.add_member(new_member)
    return jsonify({'new_member': new_member}), 200



@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)

    if member is not None:
        return jsonify({
            "id": member["id"],
            "first_name": member["first_name"],
            "last_name": member["last_name"],
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"]
        }), 200



                                                                                                        
 
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = jackson_family.delete_member(id)
    return jsonify({'done': True}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
