import os.path

from cryptography.fernet import Fernet
from flask import render_template, request, redirect, url_for, send_from_directory, send_file
from flask_login import login_required, current_user
from flask_uploads import UploadSet, IMAGES
from .. import db
from werkzeug.utils import secure_filename
# from ..models import File
from app.user import user_bp
from .forms import SingleFileForm, NewFiles
from .utils import encrypt_file_content, allowed_file, decrypt_file_content
from ..models import File

basedir = os.path.abspath(os.path.dirname(__file__))
# app.config.update(
UPLOADED_PATH = os.path.join(basedir, 'uploads')


@user_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', title='Tableau de bord')


@user_bp.route('/new-file', methods=['GET', 'POST'])
@login_required
def new_file():
    return render_template('new-file.html', title='Nouveau fichier')


@user_bp.route('/upload', methods=['POST'])
@login_required
def handle_upload():
    simple_form = SingleFileForm()
    user_upload_folder = os.path.join(UPLOADED_PATH, 'user_' + current_user.get_id())
    if request.method == 'POST':
        if not os.path.exists(user_upload_folder):
            os.makedirs(user_upload_folder)
        for key, file in request.files.items():
            original_file_name = file.filename
            file.filename = secure_filename(file.filename)
            if key.startswith('file') and allowed_file(file.filename):
                file.save(os.path.join(user_upload_folder, file.filename))
                print((os.path.getsize(user_upload_folder + '\\' + file.filename)) / 1024)
                encrypt_file_content(user_upload_folder + '\\' + file.filename)
                print((os.path.getsize(user_upload_folder + '\\' + file.filename)) / 1024)
                file_size_stored = os.path.getsize(user_upload_folder + '\\' + file.filename)
                print(file.content_type)
                n_file = File(
                    name=original_file_name,
                    path=user_upload_folder + '\\' + file.filename,
                    size=file_size_stored,
                    owner=current_user.get_id()
                )
                #             description=simple_form.description.data,
                #             owner=current_user.get_id())
                db.session.add(n_file)
                db.session.commit()
            elif not allowed_file(file.filename):
                print('file not allowed')
            else:
                print('nothing')

    return redirect(url_for('user_bp.new_file'))


@user_bp.route('/download/<id_file>', methods=['GET'])
@login_required
def download(id_file):
    file = File.query.filter_by(id=id_file).first()
    decrypt_file_content(file.path)
    return send_file(file.path, as_attachment=True)


@user_bp.route('/download-many/<id_file>', methods=['GET'])
@login_required
def download_many(id_file):
    file = File.query.filter_by(id=id_file).first()
    decrypt_file_content(file.path)
    return send_file(file.path, as_attachment=True)


@user_bp.route('/delete/<id_file>', methods=['GET'])
@login_required
def delete(id_file):
    file = File.query.filter_by(id=id_file).first()
    db.session.delete(file)
    db.session.commit()
    return redirect(url_for('user_bp.my_files'))


@user_bp.route('file-list', methods=['GET'])
@login_required
def my_files():
    files = File.query.filter_by(owner=current_user.get_id()).all()
    return render_template('files-list.html', title='Mes fichiers', files=files)


@user_bp.route('folders', methods=['GET', 'POST'])
@login_required
def folders():
    return render_template('folders.html', title='Importer des Dossiers')


@user_bp.route('new-space', methods=['GET', 'POST'])
@login_required
def new_space():
    return render_template('share-space.html', title='Paramètres')


@user_bp.route('settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html', title='Paramètres')


@user_bp.route('trash', methods=['GET', 'POST'])
@login_required
def trash():
    return render_template('trash.html', title='Corbeille')
