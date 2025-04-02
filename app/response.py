from flask import jsonify

def success(values, message):
    res = {
        "status": 200,
        "message": message,
        "data": values
    }
    return jsonify(res), 200

def badRequest(values, message):
    res = {
        "status": 400,
        "message": message,
        "data": values
    }
    return jsonify(res), 400
