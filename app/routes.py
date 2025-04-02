from app import app
from app.controller import DosenController, UserController
from flask import request

@app.route('/')
def index():
    return 'hello flask app'

@app.route('/dosen', methods=['GET', 'POST'])
def dosens():
    if request.method == 'GET':
        return DosenController.index()
    return DosenController.save()

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
