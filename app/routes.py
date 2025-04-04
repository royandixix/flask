from app import app
from app.controller import DosenController, UserController
from flask import request
from flask import jsonify
from flask_jwt_extended import get_jwt_identity  
from flask_jwt_extended import jwt_required

@app.route('/')
def index():
    return 'hello flask app'

@app.route("/protected", methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"current_user": current_user, "message": "Sukses"}), 200  # ✅ Gunakan jsonify

@app.route('/dosen', methods=['GET', 'POST'])
def dosens():
    if request.method == 'GET':
        return DosenController.index()
    return DosenController.save()

@app.route('/api/dosen/page', methods=['GET'])
def pagination():
    return DosenController.paginate()

@app.route('/file-upload', methods=['POST'])
def upload_file():
    return UserController.upload()

# @app.route('/createadmin', methods=['POST'])
# def admins():
#     return UserController.buatAdmin()

@app.route('/dosen/<id>', methods=['GET', 'PUT', 'DELETE'])
def dosenDetail(id):
    if request.method == 'GET':
        return DosenController.detail(id)
    if request.method == 'PUT':
        return DosenController.ubah(id)
    return DosenController.hapus(id)

@app.route('/login', methods=['POST'])
def logins():
    return UserController.login()

if __name__ == '__main__':
    app.run(debug=True)
