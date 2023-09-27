import unittest
from flask_testing import TestCase
from flask import url_for
from datakar import app, db, Karyawan  # Import modul-modul yang diperlukan

# Kelas MyTest untuk melakukan testing pada aplikasi
class MyTest(TestCase):

    # Metode untuk membuat aplikasi dalam mode testing
    def create_app(self):
        app.config['TESTING'] = True  # Mengaktifkan mode testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///karbca.db'  # Menggunakan database in-memory untuk testing
        return app

    # Metode yang dijalankan sebelum setiap test
    def setUp(self):
        db.create_all()  # Membuat semua tabel dalam database

    # Metode yang dijalankan setelah setiap test
    def tearDown(self):
        db.session.remove()  # Menghapus sesi database
        db.drop_all()  # Menghapus semua tabel dalam database

    # Test untuk endpoint index '/'
    def test_index(self):
        response = self.client.get('/')  # Melakukan request GET ke '/'
        self.assert200(response)  # Memastikan response adalah 200 OK
        self.assert_template_used('index.html')  # Memastikan template yang digunakan adalah 'index.html'

    # Test untuk membuat karyawan baru
    def test_create_karyawan(self):
        # Melakukan request POST ke '/karyawan' dengan data karyawan baru
        response = self.client.post('/karyawan', json={
            'nama_karyawan': 'John Doe',
            'cabang_bca': 'Jakarta',
            'jabatan': 'Staff'
        })
        self.assertStatus(response, 201)  # Memastikan response adalah 201 Created
        karyawan = Karyawan.query.first()  # Mengambil karyawan pertama dari database
        self.assertEqual(karyawan.nama_karyawan, 'John Doe')  # Memastikan nama karyawan adalah 'John Doe'

    # Test untuk menghapus karyawan
    def test_delete_karyawan(self):
        # Membuat objek karyawan baru dan menyimpannya ke database
        karyawan = Karyawan(nama_karyawan='Prast', cabang_bca='Jakarta', jabatan='Staff')
        db.session.add(karyawan)
        db.session.commit()

        # Melakukan request DELETE ke '/karyawan/{id_karyawan}'
        response = self.client.delete(f'/karyawan/{karyawan.id_karyawan}')
        self.assert200(response)  # Memastikan response adalah 200 OK
        self.assertIsNone(Karyawan.query.get(karyawan.id_karyawan))  # Memastikan karyawan dengan id tersebut sudah dihapus

    # Test untuk mendapatkan semua karyawan
    def test_get_all_karyawan(self):
        # Membuat dua objek karyawan baru dan menyimpannya ke database
        karyawan1 = Karyawan(nama_karyawan='John Doe', cabang_bca='Jakarta', jabatan='Staff')
        karyawan2 = Karyawan(nama_karyawan='Jane Doe', cabang_bca='Bandung', jabatan='Manager')
        db.session.add(karyawan1)
        db.session.add(karyawan2)
        db.session.commit()

        # Melakukan request GET ke '/display_all'
        response = self.client.get('/display_all')
        self.assert200(response)  # Memastikan response adalah 200 OK
        self.assert_template_used('displayall.html')  # Memastikan template yang digunakan adalah 'displayall.html'
        self.assertIn(b'John Doe', response.data)  # Memastikan 'John Doe' ada dalam response data
        self.assertIn(b'Jane Doe', response.data)  # Memastikan 'Jane Doe' ada dalam response data

    # Test untuk mendapatkan satu karyawan berdasarkan id
    def test_get_one_karyawan(self):
        # Membuat objek karyawan baru dan menyimpannya ke database
        karyawan = Karyawan(nama_karyawan='John Doe', cabang_bca='Jakarta', jabatan='Staff')
        db.session.add(karyawan)
        db.session.commit()

        # Melakukan request GET ke '/karyawan/{id_karyawan}'
        response = self.client.get(f'/karyawan/{karyawan.id_karyawan}')
        self.assert200(response)  # Memastikan response adalah 200 OK

    # Test untuk menghapus karyawan melalui UI
    def test_delete_karyawan_ui(self):
        # Membuat objek karyawan baru dan menyimpannya ke database
        karyawan = Karyawan(nama_karyawan='John Doe', cabang_bca='Jakarta', jabatan='Staff')
        db.session.add(karyawan)
        db.session.commit()

        # Melakukan request POST ke '/delete_karyawan' dengan data nama karyawan
        response = self.client.post('/delete_karyawan', data={'nama_karyawan': 'John Doe'})
        self.assert200(response)  # Memastikan response adalah 200 OK
        self.assert_template_used('deletedata.html')  # Memastikan template yang digunakan adalah 'deletedata.html'
        self.assertIn(b'John Doe', response.data)  # Memastikan 'John Doe' ada dalam response data

if __name__ == '__main__':
    unittest.main()  # Menjalankan semua test