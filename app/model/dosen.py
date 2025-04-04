from app import db

class Dosen(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nidn = db.Column(db.String(300), nullable=False)
    nama = db.Column(db.String(399), nullable=False)
    phone = db.Column(db.String(13), nullable=False)
    alamat = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Dosen {self.name}>'
 