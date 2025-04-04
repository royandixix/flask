from app.model.dosen import Dosen
from app.model.mahasiswa import Mahasiswa
from app import app, db  # Jangan impor 'response' di sini
from flask import request
from sqlalchemy import or_  # Diperlukan untuk OR filter
from flask import jsonify
import math


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
    

    
def get_pagination(clss, url, start, limit):
    #ambil data select
    results = clss.query.all()
    #ubah format
    data = formatarray(results)
    #hitung jumlah data
    count = len(data)

    obj = {}
    if count < start:
        obj['success'] = False
        obj['message'] = "Page yang dipilih melewati batas total data!"
        return obj
    else:
        obj['success'] = True
        obj['start_page'] = start
        obj['per_page'] = limit
        obj['total_data'] = count

        #previous link
        if start == 1:
            obj['previous'] = ''
        else:
            start_copy = max(1, start - limit)
            limit_copy = start - 1
            obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)

        #next link
        if start + limit > count:
            obj['next'] = ''
        else:
            start_copy = start + limit
            obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)

        obj['results'] = data[(start - 1):(start - 1 + limit)]
        return obj 

def paginate():
    #ambil parameter get 
    #sample www.google.com?product=baju

    start = request.args.get('start')
    limit = request.args.get('limit')

    try:
        if start is None or limit is None:
            return jsonify(get_pagination(
                Dosen,
                'http://127.0.0.1:5000/api/dosen/page',
                start=1,
                limit=3
            ))
        else:
            return jsonify(get_pagination(
                Dosen,
                'http://127.0.0.1:5000/api/dosen/page',
                start=int(start),
                limit=int(limit)
            ))
    except Exception as e:
        print(e)
