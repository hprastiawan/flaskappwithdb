import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table

DATABASE_URI = 'mysql://root:m1B14fwDsBDtwMYS7x12@containers-us-west-167.railway.app:7090/railway'
engine = create_engine(DATABASE_URI, echo=True)
metadata = MetaData()

# Mendefinisikan tabel 'karyawan'
karyawan = Table('karyawan', metadata,
    Column('id_karyawan', Integer, primary_key=True),
    Column('nama_karyawan', String),
    Column('cabang_bca', String),
    Column('jabatan', String)
)

# Membuat tabel
metadata.create_all(engine)

print("Database karbca.db dan tabel karyawan telah berhasil dibuat!")
