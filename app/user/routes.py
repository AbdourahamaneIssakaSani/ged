import os.path
import datetime

from flask import render_template, request, redirect, url_for, send_file, app
from flask_login import login_required, current_user
from flask_uploads import AUDIO, TEXT, IMAGES, ARCHIVES
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
from app.user import user_bp
from .utils import encrypt_file_content, allowed_file, decrypt_file_content
from .. import db
from .. import create_app
from ..models import File, Folder, SharingSpace, Message, SpaceFiles, SpaceFolders, User, Members

basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_PATH = os.path.join(basedir, 'uploads')


# UPLOAD_PROFILE_PHOTO_PATH = os.path.join(app.static_url_path, 'uploads')


@user_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user_upload_folder = os.path.join(UPLOAD_PATH, 'user_' + current_user.get_id())
    total_size = 0
    if os.path.exists(user_upload_folder):
        for path, dirs, files in os.walk(user_upload_folder):
            for f in files:
                fp = os.path.join(path, f)
                total_size += os.stat(fp).st_size
    files_number = len(File.query.filter_by(folder=None, owner=current_user.id).all())
    shared_files_number = len(File.query.filter_by(is_shared=1, owner=current_user.id).all())
    folders_number = len(Folder.query.filter_by(owner=current_user.id).all())
    folder_files_number = len(File.query.filter(File.folder is not None).filter_by(owner=current_user.id).all())
    print('folder_files_number :')
    print(folder_files_number)
    shared_folders_number = len(Folder.query.filter_by(is_shared=1, owner=current_user.id).all())
    spaces_number = len(SharingSpace.query.filter_by(admin=current_user.id).all())
    archived_spaces_number = len(SharingSpace.query.filter_by(admin=current_user.id, is_archived=1).all())
    members_number = 0
    for member in Members.query.all():
        members_number += len(SharingSpace.query.filter_by(id=member.space, admin=current_user.id).all())
    return render_template(
        'dashboard.html',
        title='Tableau de bord',
        total_size=total_size,
        files_number=files_number,
        shared_files_number=shared_files_number,
        folders_number=folders_number,
        folder_files_number=folder_files_number,
        shared_folders_number=shared_folders_number,
        spaces_number=spaces_number,
        archived_spaces_number=archived_spaces_number,
        members_number=members_number
    )


@user_bp.route('/new-file', methods=['GET', 'POST'])
@login_required
def new_file():
    return render_template('new-file.html', title='Nouveau fichier')


@user_bp.route('/new-folder', methods=['POST'])
@login_required
def new_folder():
    if request.method == 'POST':
        original_name = request.form['name']
        user_upload_folder = os.path.join(UPLOAD_PATH, 'user_' + current_user.get_id())
        if not os.path.exists(user_upload_folder):
            os.makedirs(user_upload_folder)
        folder = os.path.join(user_upload_folder, secure_filename(original_name))
        if not os.path.exists(folder):
            os.makedirs(folder)
            n_folder = Folder(name=original_name, path=folder, owner=current_user.id)
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
            n_folder = Folder(name=original_name, path=child_folder, parent_folder=id_folder, owner=current_user.id)
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
                file_type = icon_file_type(folder.path + '\\' + file.filename)
                n_file = File(
                    name=original_file_name,
                    path=folder.path + '\\' + file.filename,
                    size=file_stored_size,
                    type=file_type,
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
    user_upload_folder = os.path.join(UPLOAD_PATH, 'user_' + current_user.get_id())
    if request.method == 'POST':
        if not os.path.exists(user_upload_folder):
            os.makedirs(user_upload_folder)
        for key, file in request.files.items():
            original_file_name = file.filename
            file.filename = secure_filename(file.filename)
            if key.startswith('file') and allowed_file(file.filename):
                file.save(os.path.join(user_upload_folder, file.filename))
                encrypt_file_content(user_upload_folder + '\\' + file.filename)
                file_size_stored = os.path.getsize(user_upload_folder + '\\' + file.filename)
                file_type = icon_file_type(user_upload_folder + '\\' + file.filename)
                n_file = File(
                    name=original_file_name,
                    path=user_upload_folder + '\\' + file.filename,
                    size=file_size_stored,
                    type=file_type,
                    owner=current_user.get_id()
                )
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


@user_bp.route('/open-file/<id_file>', methods=['GET'])
@login_required
def open_file(id_file):
    file = File.query.filter_by(id=id_file).first()
    decrypt_file_content(file.path)
    return send_file(file.path)


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


@user_bp.route('/folder-to-trash/<id_folder>', methods=['GET'])
@login_required
def move_folder_to_trash(id_folder):
    folder = File.query.filter_by(id=id_folder).first()
    folder.is_deleted = 1
    folder.delete_date = datetime.datetime.now().date()
    db.session.commit()
    return redirect(url_for('user_bp.my_folders'))


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
    spaces = SharingSpace.query.filter_by(admin=current_user.id).all()
    return render_template('files-list.html', title='Mes fichiers', files=files, spaces=spaces)


def sub_folders(folder, n=1):
    if folder.folders:
        for child_folder in folder.folders:
            print('-' * n + child_folder.name)
        n += 1
        for child_folder in folder.folders:
            sub_folders(child_folder, n)


@user_bp.route('folders', methods=['GET', 'POST'])
@login_required
def my_folders():
    folders = Folder.query.filter_by(parent_folder=None, owner=current_user.id).all()
    spaces = SharingSpace.query.filter_by(admin=current_user.id).all()

    return render_template(
        'folders.html',
        title='Mes Dossiers',
        folders=folders,
        spaces=spaces
    )


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
    spaces = SharingSpace.query.filter_by(is_archived=0, admin=current_user.id).all()
    sp_mem = Members.query.filter_by(id=current_user.id).all()
    guest_spaces = []
    for id_space in sp_mem:
        space = SharingSpace.query.filter_by(id=id_space.space, is_archived=0).first()
        guest_spaces.append(space)
    return render_template(
        'share-space.html',
        title='Mes Espaces',
        spaces=spaces,
        guest_spaces=guest_spaces
    )


@user_bp.route('space/<id_space>', methods=['GET', 'POST'])
@login_required
def space_content(id_space):
    space = SharingSpace.query.filter_by(id=id_space, is_archived=0).first()
    folders = Folder.query.filter_by(parent_folder=None, owner=current_user.id).all()
    files = File.query.filter_by(folder=None, owner=current_user.id).all()
    users = User.query.filter(User.id != current_user.get_id()).all()

    return render_template(
        'space-content.html',
        title='Espace',
        space=space,
        folders_to_share=folders,
        files_to_share=files,
        users=users
    )


@user_bp.route('space-folder/<id_space>', methods=['GET'])
@login_required
def shared_folders(id_space):
    space = SharingSpace.query.filter_by(id=id_space, is_archived=0).first()
    folders = Folder.query.filter_by(parent_folder=None).all()
    files = File.query.filter_by(folder=None, owner=current_user.id).all()
    users = User.query.filter(User.id != current_user.id).all()
    space_folders = []
    temp_folders = SpaceFolders.query.filter_by(space=id_space).all()
    for id_folder in temp_folders:
        folder = Folder.query.filter_by(id=id_folder.folder).first()
        space_folders.append(folder)
    return render_template(
        'shared-folders.html',
        title='Espace',
        space=space,
        space_folders=space_folders,
        folders_to_share=folders,
        files_to_share=files,
        users=users
    )


@user_bp.route('space-members/<id_space>', methods=['GET'])
@login_required
def space_members(id_space):
    space = SharingSpace.query.filter_by(id=id_space, is_archived=0).first()
    folders = Folder.query.filter_by(parent_folder=None, owner=current_user.id).all()
    files = File.query.filter_by(folder=None, owner=current_user.id).all()
    users = User.query.filter(User.id != current_user.get_id()).all()

    members = Members.query.filter_by(space=id_space).all()

    return render_template(
        'members.html',
        title='Membres',
        members=members,
        space=space,
        folders_to_share=folders,
        files_to_share=files,
        users=users
    )


@user_bp.route('share-file', methods=['POST'])
@login_required
def share_file():
    file_id = request.form['file_id']
    space_id = request.form['space_id']
    space_file = SpaceFiles(file=file_id, space=space_id)
    file = File.query.filter_by(id=file_id).first()
    file.is_shared = 1
    db.session.add(space_file)
    db.session.commit()
    return redirect(url_for('user_bp.my_spaces'))


@user_bp.route('add-member', methods=['POST'])
@login_required
def add_member():
    member_id = request.form['member_id']
    space_id = request.form['space_id']
    user = User.query.filter_by(id=member_id).first()
    member = Members(id=member_id, first_name=user.first_name, last_name=user.last_name, email=user.email,
                     space=space_id)
    db.session.add(member)
    db.session.commit()
    return redirect(url_for('user_bp.my_spaces'))


@user_bp.route('shared-files/<id_space>', methods=['GET'])
@login_required
def shared_files(id_space):
    space = SharingSpace.query.filter_by(id=id_space, is_archived=0).first()
    files = SpaceFiles.query.filter_by(space=id_space).all()
    space_files = []
    for id_file in files:
        file = File.query.filter_by(id=id_file.file).first()
        space_files.append(file)
    return render_template(
        'shared-files.html',
        title='Fichiers partagés',
        space=space,
        space_files=space_files,
    )


@user_bp.route('share-folder', methods=['POST'])
@login_required
def share_folder():
    folder_id = request.form['folder_id']
    space_id = request.form['space_id']
    space_folder = SpaceFolders(folder=folder_id, space=space_id)
    folder = Folder.query.filter_by(id=folder_id).first()
    folder.is_shared = 1
    db.session.add(space_folder)
    db.session.commit()
    return redirect(url_for('user_bp.my_spaces'))


@user_bp.route('new-photo', methods=['POST'])
@login_required
def profile_photo():
    print('enter')
    profile_photo_folder = os.path.join(create_app().static_url_path, 'user_' + current_user.get_id())
    profile_photo_folder = profile_photo_folder.replace('/', '\\')
    print(profile_photo_folder)
    if not os.path.exists(profile_photo_folder):
        os.makedirs(profile_photo_folder)
        print('mkdir')
    for key, file in request.files.items():
        file.filename = secure_filename(file.filename)
        print('secure')
        if key.startswith('file'):
            file.filename = secure_filename(file.filename)
            print('saviiiiiiiiiiiiiiing')
            file.save(os.path.join(profile_photo_folder, file.filename))
            user = User.query.filter_by(id=current_user.id).first()
            user.photo = file.filename
            db.session.commit()
    return redirect(url_for('user_bp.settings'))


@user_bp.route('settings', methods=['GET', 'POST'])
@login_required
def settings():
    settings_errors = {}
    if request.form == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        birthday = request.form['birthday']
        gender = request.form['gender']
        password = request.form['password']
        new_password = request.form['new_password']
        user = User.query.filter_by(id=current_user.id).first()
        member = Members.query.filter_by(id=current_user.id).first()
        if first_name:
            user.first_name = first_name
            member.first_name = first_name
        if last_name:
            user.last_name = last_name
            member.last_name = last_name
        if email:
            user.email = email
            member.email = email
        if phone:
            user.phone = phone
            member.phone = phone
        if birthday:
            user.birthday = birthday
            member.birthday = birthday
        if gender:
            user.gender = gender
            member.gender = gender
        if new_password:
            if user.verify_password(password):
                user.password = new_password
            else:
                settings_errors.update({"password": "Mot de passe incorrect! Réessayez"})
        db.session.commit()
    return render_template('settings.html', title='Paramètres', settings_errors=settings_errors)


@user_bp.route('trash', methods=['GET', 'POST'])
@login_required
def trash():
    files = File.query.filter_by(owner=current_user.get_id(), is_deleted=1).all()
    folders = Folder.query.filter_by(is_deleted=1).all()
    return render_template('trash.html', title='Corbeille', files=files, folders=folders)
