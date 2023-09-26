from flask import Flask, jsonify, request, render_template
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from
import os

app = Flask(__name__)

# Konfigurasi database
app.config['SQLALCHEMY_ECH0'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:m1B14fwDsBDtwMYS7x12@containers-us-west-167.railway.app:7090/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Konfigurasi Swagger
app.config['SWAGGER'] = {
    'title': 'Data Karyawan BCA API',
    'uiversion': 3,
    'headers': [],
    'specs': [
        {
            'endpoint': 'apispec_1',
            'route': '/apispec_1.json',
            'rule_filter': lambda rule: True,
            'model_filter': lambda tag: True,
        }
    ],
    'static_url_path': '/flasgger_static',
    'swagger_ui': True,
    'specs_route': '/apidocs/'
}
swagger = Swagger(app)

db = SQLAlchemy(app)

# Model Data Karyawan
class Karyawan(db.Model):
    id_karyawan = db.Column(db.Integer, primary_key=True)
    nama_karyawan = db.Column(db.String(100), nullable=False)
    cabang_bca = db.Column(db.String(100), nullable=False)
    jabatan = db.Column(db.String(100), nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/karyawan', methods=['POST'])
@swag_from('swagger_docs/create_data_bca.yaml')
def create_karyawan():
    # Mendapatkan data dari permintaan POST
    data = request.json

    # Validasi data sesuai kebutuhan

    # Membuat objek Karyawan
    new_karyawan = Karyawan(
        nama_karyawan=data['nama_karyawan'],
        cabang_bca=data['cabang_bca'],
        jabatan=data['jabatan']
    )

    # Menyimpan objek ke database
    db.session.add(new_karyawan)
    db.session.commit()

    # Mengembalikan respons HTTP 201 Created
    return jsonify({'message': 'Data karyawan berhasil ditambahkan'}), 201

@app.route('/karyawan/<int:id_karyawan>', methods=['DELETE'])
@swag_from('swagger_docs/delete_data_bca.yaml')
def delete_karyawan(id_karyawan):
    try:
        # Cari karyawan berdasarkan id_karyawan
        karyawan_to_delete = Karyawan.query.filter_by(id_karyawan=id_karyawan).first()

        # Jika karyawan ditemukan, hapus dari database
        if karyawan_to_delete:
            db.session.delete(karyawan_to_delete)
            db.session.commit()
            return jsonify({'message': f'Data karyawan dengan ID {id_karyawan} berhasil dihapus'}), 200
        else:
            return jsonify({'message': f'Data karyawan dengan ID {id_karyawan} tidak ditemukan'}), 404
    except Exception as e:
        return jsonify({'message': f"Terjadi kesalahan: {e}"}), 500


@app.route('/display_all', methods=['GET'])
@swag_from('swagger_docs/get_all_data.yaml')
def get_all_karyawan():
    karyawan_list = []
    try:
        # Mengambil semua data karyawan dari database
        all_karyawan = Karyawan.query.all()

        # Membuat daftar dari data karyawan untuk dikirimkan ke template
        for karyawan in all_karyawan:
            karyawan_data = {
                'id_karyawan': karyawan.id_karyawan,
                'nama_karyawan': karyawan.nama_karyawan,
                'cabang_bca': karyawan.cabang_bca,
                'jabatan': karyawan.jabatan
            }
            karyawan_list.append(karyawan_data)

    except Exception as e:
        # Mengembalikan pesan kesalahan dalam Bahasa Indonesia jika terjadi kesalahan
        return render_template('error.html', pesan="Terjadi kesalahan saat mengambil data karyawan: {}".format(str(e))), 500

    finally:
        # Mengembalikan template dengan data karyawan jika tidak ada kesalahan
        if karyawan_list:
            return render_template('displayall.html', karyawan_list=karyawan_list)
        else:
            # Mengembalikan pesan kesalahan dalam Bahasa Indonesia jika tidak ada data karyawan
            return render_template('error.html', pesan="Tidak ada data karyawan yang dapat ditampilkan."), 404

@app.route('/karyawan/<int:id_karyawan>', methods=['GET'])
@swag_from('swagger_docs/get_one_bca.yaml')
def get_one_karyawan(id_karyawan):
    # Implementasi fungsi untuk mengambil data karyawan berdasarkan id_karyawan
    pass

@app.route('/update_karyawan', methods=['POST'])
def update_karyawan():
    try:
        # Ambil data dari form
        id_karyawan = request.form.get('id_karyawan')
        nama_karyawan = request.form.get('nama_karyawan')
        cabang_bca = request.form.get('cabang_bca')
        jabatan = request.form.get('jabatan')
        
        # Temukan karyawan berdasarkan id_karyawan
        karyawan = Karyawan.query.get(id_karyawan)
        
        if not karyawan:
            return jsonify({'message': 'Karyawan tidak ditemukan'}), 404
        
        # Update data karyawan
        karyawan.nama_karyawan = nama_karyawan
        karyawan.cabang_bca = cabang_bca
        karyawan.jabatan = jabatan
        
        # Simpan perubahan ke database
        db.session.commit()
        
        return redirect(url_for('get_all_karyawan'))
        # return jsonify({'message': 'Data karyawan berhasil diperbarui'}), 200
    except Exception as e:
        return jsonify({'message': f'Terjadi kesalahan: {str(e)}'}), 500

@app.route('/input', methods=['GET', 'POST'])
def input_data():
    if request.method == 'POST':
        # Mendapatkan data dari form
        nama_karyawan = request.form.get('nama_karyawan')
        cabang_bca = request.form.get('cabang_bca')
        jabatan = request.form.get('jabatan')

        # Membuat objek Karyawan
        new_karyawan = Karyawan(
            nama_karyawan=nama_karyawan,
            cabang_bca=cabang_bca,
            jabatan=jabatan
        )

        # Menyimpan objek ke database
        db.session.add(new_karyawan)
        db.session.commit()

        # Mengarahkan ke halaman konfirmasi
        return render_template('confirmation.html')

    # Jika metode request adalah GET, tampilkan form input data
    return render_template('createdata.html')

@app.route('/updatedata', methods=['GET', 'POST'])
def updatedata():
    if request.method == 'POST':
        nama_karyawan = request.form.get('nama_karyawan')
        data_list = Karyawan.query.filter(Karyawan.nama_karyawan.like(f"%{nama_karyawan}%")).all()
        return render_template('updatedatakar.html', data_list=data_list)
    return render_template('updatedatakar.html')

@app.route('/delete_karyawan', methods=['GET', 'POST'])
def delete_karyawan_ui():
    data_list = []
    try:
        if request.method == 'POST':
            search_name = request.form['nama_karyawan'].lower()
            all_karyawan = Karyawan.query.all()
            data_list = [karyawan for karyawan in all_karyawan if search_name in karyawan.nama_karyawan.lower()]
    except Exception as e:
        error_message = f"Terjadi kesalahan: {e}"
        print(error_message)
        return render_template('error.html', pesan=error_message), 500
    finally:
        return render_template('deletedata.html', data_list=data_list)

if __name__ == '__main__':
    app.run(debug=True)
