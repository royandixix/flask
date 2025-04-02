import os

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Menyesuaikan pengaturan untuk host dan port
    HOST = os.environ.get("DB_HOST", "localhost").split(':')[0]  # Hanya ambil alamat host
    PORT = os.environ.get("DB_HOST", "localhost").split(':')[1] if ':' in os.environ.get("DB_HOST", "") else "3306"  # Menambahkan pengaturan port
    DATABASE = os.environ.get("DB_DATABASE", "db_flask")
    USERNAME = os.environ.get("DB_USERNAME", "root")
    PASSWORD = os.environ.get("DB_PASSWORD", "")

    # Pastikan JWT_SECRET_KEY memiliki fallback
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET", "default_secret_key")  # Default jika tidak ada

    # Pengaturan URL koneksi ke database MySQL
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True  # Mengaktifkan pencatatan query untuk debugging
