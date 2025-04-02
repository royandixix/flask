from app.model.dosen import Dosen
from app.model.mahasiswa import Mahasiswa
from app import app, db  # Jangan impor 'response' di sini
from flask import request
from sqlalchemy import or_  # Diperlukan untuk OR filter


def index():
    try:
        from app import response  # Impor di dalam fungsi untuk menghindari circular import
        dosen = Dosen.query.all()
        data = formatarray(dosen)
        return response.success(data, "success")
    except Exception as e:
        print(e)
        return response.badRequest([], str(e))


def formatarray(datas):
    array = []
    for i in datas:
        array.append(singleObject(i))
    return array  


def singleObject(data):
    return {
        'id': data.id,
        'nidn': data.nidn,
        'nama': data.nama,
        'phone': data.phone,
        'alamat': data.alamat
    }


def detail(id):
    try:
        from app import response
        dosen = Dosen.query.filter_by(id=id).first()
        mahasiswa = Mahasiswa.query.filter(
            or_(
                Mahasiswa.dosen_satu == id,
                Mahasiswa.dosen_dua == id
            )
        ).all()

        if not dosen:
            return response.badRequest([], 'Tidak ada dosen')

        datamahasiswa = formatmahasiswa(mahasiswa)
        data = SingleDetailMahasiswa(dosen, datamahasiswa)
        return response.success(data, "success")

    except Exception as e:
        print(e)
        return response.badRequest([], str(e))


def SingleDetailMahasiswa(dosen, mahasiswa):
    return {
        'id': dosen.id,
        'nidn': dosen.nidn,
        'nama': dosen.nama,
        'phone': dosen.phone,
        'alamat': dosen.alamat,
        'mahasiswa': mahasiswa
    }


def singleMahasiswa(mahasiswa):
    return {
        'id': mahasiswa.id,
        'nim': mahasiswa.nim,
        'nama': mahasiswa.nama,
        'phone': mahasiswa.phone
    }


def formatmahasiswa(data):
    array = []
    for i in data: 
        array.append(singleMahasiswa(i))
    return array


def save():
    try:
        from app import response
        nidn = request.form.get('nidn')
        nama = request.form.get('nama')
        phone = request.form.get('phone')
        alamat = request.form.get('alamat')

        dosens = Dosen(nidn=nidn, nama=nama, phone=phone, alamat=alamat)
        db.session.add(dosens)
        db.session.commit()

        return response.success('', 'sukses Menambahkan Data dosen ')
    except Exception as e:
        print(e)
        return response.badRequest([], str(e))


def ubah(id):
    try:
        from app import response
        nidn = request.form.get('nidn')
        nama = request.form.get('nama')
        phone = request.form.get('phone')
        alamat = request.form.get('alamat')

        input = [
            {
                'nidn': nidn,
                'nama': nama,
                'phone': phone,
                'alamat': alamat,
            }
        ]

        dosen = Dosen.query.filter_by(id=id).first()

        dosen.nidn = nidn
        dosen.nama = nama
        dosen.phone = phone
        dosen.alamat = alamat

        db.session.commit()
        return response.success(input, 'sukses update data ')
    except Exception as e:
        print(e)
        return response.badRequest([], str(e))


def hapus(id):
    try:
        from app import response
        dosen = Dosen.query.filter_by(id=id).first()
        if not dosen:
            return response.badRequest([], 'Data Dosen Kosong')

        db.session.delete(dosen)
        db.session.commit()

        return response.success('', 'Berhasil menghapus data!')
    except Exception as e:
        print(e)
        return response.badRequest([], str(e))
