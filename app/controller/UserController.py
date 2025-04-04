from app.model.user import User
from app.model.gambar import Gambar
import os
from app import response, app, db, uploadconfig
from flask import request
import datetime
from flask_jwt_extended import create_access_token, create_refresh_token
import uuid
from werkzeug.utils import secure_filename


def upload():
    try:
        judul = request.form.get('judul')

        if 'file' not in request.files:
            return response.badRequest([], 'File tidak tersedia')

        file = request.files['file']

        if file.filename == '':
            return response.badRequest([], 'File tidak tersedia')

        if file and uploadconfig.allowed_file(file.filename):
            uid = uuid.uuid4()
            filename = "flask-" + str(uid) + "-" + file.filename

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            uploads = Gambar(judul=judul, pathname=filename)
            db.session.add(uploads)
            db.session.commit()

            return response.success(
                {
                    'judul': judul,
                    'pathname': filename
                },
                "Sukses mengupload file"
            )
        else:
            return response.badRequest([], 'File tidak diizinkan')

    except Exception as e:
        print(e)
        return response.badRequest([], 'Terjadi kesalahan pada server')


def buatAdmin():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        level = 1

        # Membuat instance user baru
        users = User(name=name, email=email, level=level)
        
        # Mengatur password dengan setPassword
        users.setPassword(password)
        
        # Menambahkan user ke database
        db.session.add(users)
        db.session.commit()

        # Mengembalikan respon suksses
        return response.success('', 'Sukses menambahkan data')
    except Exception as e:
        print(e)
        return response.badRequest([], 'Terjadi kesalahan saat menambahkan data')

def singleObject(data):
    """Mengembalikan data user dalam format dictionary"""
    return {
        'id': data.id,
        'name': data.name,
        'email': data.email,
        'level': data.level
    }


def login():
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        # Mencari user berdasarkan email
        user = User.query.filter_by(email=email).first()
        
        # Jika user tidak ditemukan
        if not user:
            return response.badRequest([], 'Email tidak terdaftar')
        
        # Jika password salah
        if not user.checkPassword(password):
            return response.badRequest([], 'Kombinasi password salah')

        # Membuat data user dalam format dictionary
        data = singleObject(user)
        
        # Waktu kadaluarsa token (7 hari)
        expires = datetime.timedelta(days=7)
        expires_refresh = datetime.timedelta(days=7)  # Perbaiki penulisan 'timedate' menjadi 'timedelta'

        # Membuat access token dan refresh token
        access_token = create_access_token(identity=user.id, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(identity=user.id, expires_delta=expires_refresh)

        # Mengembalikan response sukses
        return response.success({
            "data": data,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, "Sukses login!")
    except Exception as e:
        print(e)
        return response.badRequest([], 'Terjadi kesalahan saat login')

