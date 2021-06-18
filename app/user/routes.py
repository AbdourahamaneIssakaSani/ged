import os.path
import datetime

from flask import render_template, request, redirect, url_for, send_file
from flask_login import login_required, current_user
from flask_uploads import AUDIO, TEXT, IMAGES, ARCHIVES
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
from app.user import user_bp
from .utils import encrypt_file_content, allowed_file, decrypt_file_content
from .. import db
from ..models import File, Folder, SharingSpace, Message, SpaceFiles, SpaceFolders

basedir = os.path.abspath(os.path.dirname(__file__))

UPLOADED_PATH = os.path.join(basedir, 'uploads')


@user_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', title='Tableau de bord')


@user_bp.route('/new-file', methods=['GET', 'POST'])
@login_required
def new_file():
    return render_template('new-file.html', title='Nouveau fichier')


@user_bp.route('/new-folder', methods=['POST'])
@login_required
def new_folder():
    if request.method == 'POST':
        original_name = request.form['name']
        user_upload_folder = os.path.join(UPLOADED_PATH, 'user_' + current_user.get_id())
        if not os.path.exists(user_upload_folder):
            os.makedirs(user_upload_folder)
        folder = os.path.join(user_upload_folder, secure_filename(original_name))
        if not os.path.exists(folder):
            os.makedirs(folder)
            n_folder = Folder(name=original_name, path=folder)
            db.session.add(n_folder)
            db.session.commit()

    return redirect(url_for('user_bp.my_folders'))


@user_bp.route('/new-folder-in/<id_folder>', methods=['POST'])
@login_required
def new_folder_in_folder(id_folder):
    if request.method == 'POST':
        parent_folder = Folder.query.filter_by(id=id_folder).first()
        original_name = request.form['name']
        child_folder = os.path.join(parent_folder.path, secure_filename(original_name))
        if not os.path.exists(child_folder):
            os.makedirs(child_folder)
            n_folder = Folder(name=original_name, path=child_folder, parent_folder=id_folder)
            db.session.add(n_folder)
            db.session.commit()

        return redirect(url_for('user_bp.my_folders'))


@user_bp.route('/upload-in-folder/<id_folder>', methods=['POST'])
@login_required
def upload_in_folder(id_folder):
    if request.method == 'POST':
        folder = Folder.query.filter_by(id=id_folder).first()
        for key, file in request.files.items():
            original_file_name = file.filename
            file.filename = secure_filename(file.filename)
            if key.startswith('file') and allowed_file(file.filename):
                file.save(os.path.join(folder.path, file.filename))
                encrypt_file_content(folder.path + '\\' + file.filename)
                file_stored_size = os.path.getsize(folder.path + '\\' + file.filename)
                n_file = File(
                    name=original_file_name,
                    path=folder.path + '\\' + file.filename,
                    size=file_stored_size,
                    folder=folder.id,
                    owner=current_user.get_id()
                )
                db.session.add(n_file)
                db.session.commit()
    return redirect(url_for('user_bp.my_folders'))


def icon_file_type(filename):
    file_extension = os.path.splitext(filename)[1]
    file_extension = file_extension.replace('.', '')
    supported_video_extensions = {"mp4", "webm", "mkv", "avi", "m4v", "m4p", "mpeg", "3gp"}
    supported_office_word_extensions = {"doc", "docx"}
    supported_office_powerpoint_extensions = {"ppt", "pptx"}
    supported_office_excel_extensions = {"xls", "xlsx"}
    if file_extension == 'pdf':
        return '-pdf'
    elif file_extension in AUDIO or file_extension == "m4a":
        return '-audio'
    elif file_extension in supported_video_extensions:
        return '-video'
    elif file_extension in TEXT:
        return '-alt'
    elif file_extension in IMAGES:
        return '-image'
    elif file_extension in ARCHIVES:
        return '-archive'
    elif file_extension in supported_office_word_extensions:
        return '-word'
    elif file_extension in supported_office_powerpoint_extensions:
        return '-powerpoint'
    elif file_extension in supported_office_excel_extensions:
        return '-excel'
    else:
        return ' '


@user_bp.route('/upload', methods=['POST'])
@login_required
def handle_upload():
    user_upload_folder = os.path.join(UPLOADED_PATH, 'user_' + current_user.get_id())
    if request.method == 'POST':
        if not os.path.exists(user_upload_folder):
            os.makedirs(user_upload_folder)
        for key, file in request.files.items():
            original_file_name = file.filename
            file.filename = secure_filename(file.filename)
            if key.startswith('file') and allowed_file(file.filename):
                file.save(os.path.join(user_upload_folder, file.filename))
                # print((os.path.getsize(user_upload_folder + '\\' + file.filename)) / 1024)
                encrypt_file_content(user_upload_folder + '\\' + file.filename)
                # print((os.path.getsize(user_upload_folder + '\\' + file.filename)) / 1024)
                file_size_stored = os.path.getsize(user_upload_folder + '\\' + file.filename)
                file_type = icon_file_type(user_upload_folder + '\\' + file.filename)
                # print('fichier de type : '+file_type)
                n_file = File(
                    name=original_file_name,
                    path=user_upload_folder + '\\' + file.filename,
                    size=file_size_stored,
                    type=file_type,
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


@user_bp.route('/to-trash/<id_file>', methods=['GET'])
@login_required
def move_to_trash(id_file):
    file = File.query.filter_by(id=id_file).first()
    file.is_deleted = 1
    file.delete_date = datetime.datetime.now().date()
    db.session.commit()
    return redirect(url_for('user_bp.my_files'))


@user_bp.route('/restore/<id_file>', methods=['GET'])
@login_required
def restore_file(id_file):
    file = File.query.filter_by(id=id_file).first()
    file.is_deleted = 0
    db.session.commit()
    return redirect(url_for('user_bp.trash'))


@user_bp.route('/delete/<id_file>', methods=['GET'])
@login_required
def delete(id_file):
    file = File.query.filter_by(id=id_file).first()
    os.remove(file.path)
    db.session.delete(file)
    db.session.commit()
    return redirect(url_for('user_bp.trash'))


@user_bp.route('file-list', methods=['GET'])
@login_required
def my_files():
    files = File.query.filter_by(owner=current_user.get_id(), is_deleted=0).all()
    spaces = SharingSpace.query.all()
    return render_template('files-list.html', title='Mes fichiers', files=files, spaces=spaces)


@user_bp.route('folders', methods=['GET', 'POST'])
@login_required
def my_folders():
    folders = Folder.query.filter_by(parent_folder=None).options(joinedload('files'), joinedload('folders')).all()
    return render_template('folders.html', title='Mes Dossiers', folders=folders)


@user_bp.route('new-space', methods=['POST'])
@login_required
def new_space():
    space_name = request.form['name']
    message_body = request.form['message']
    n_space = SharingSpace(name=space_name)
    message = Message(body=message_body, space=n_space, sender=current_user.get_id())
    n_space.messages.append(message)
    db.session.add(n_space)
    db.session.commit()
    return redirect(url_for('user_bp.my_spaces'))


@user_bp.route('spaces', methods=['GET', 'POST'])
@login_required
def my_spaces():
    spaces = SharingSpace.query.filter_by(is_archived=0).all()
    return render_template('share-space.html', title='Mes Espaces', spaces=spaces)


@user_bp.route('share-file', methods=['POST'])
@login_required
def share_file():
    file_id = request.form['file_id']
    space_id = request.form['space_id']
    space_file = SpaceFiles(file=file_id, space=space_id)
    db.session.add(space_file)
    db.session.commit()
    return redirect(url_for('user_bp.my_spaces'))


@user_bp.route('share-folder', methods=['POST'])
@login_required
def share_folder():
    file_id = request.form['folder_id']
    space_id = request.form['space_id']
    space_folder = SpaceFolders(file=file_id, space=space_id)
    db.session.add(space_folder)
    db.session.commit()
    return redirect(url_for('user_bp.my_spaces'))


@user_bp.route('settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html', title='Paramètres')


@user_bp.route('trash', methods=['GET', 'POST'])
@login_required
def trash():
    files = File.query.filter_by(owner=current_user.get_id(), is_deleted=1).all()
    folders = Folder.query.filter_by(is_deleted=1).all()
    return render_template('trash.html', title='Corbeille', files=files, folders=folders)
