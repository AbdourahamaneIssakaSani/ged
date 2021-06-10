import os.path

from flask import render_template, request, redirect, url_for, current_app as app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, IMAGES, AllExcept, SCRIPTS, EXECUTABLES
from cryptography.fernet import Fernet
from .. import db
# from ..models import File
from app.user import user_bp
from .forms import SingleFileForm, NewFiles
from ..models import File

ALLOWED_EXTENSIONS = AllExcept(SCRIPTS + EXECUTABLES)
basedir = os.path.abspath(os.path.dirname(__file__))
# app.config.update(
UPLOADED_PATH = os.path.join(basedir, 'uploads')
#     DROPZONE_SERVE_LOCAL=True,
#     DROPZONE_ALLOWED_FILE_CUSTOM=True,
#     DROPZONE_ALLOWED_FILE_TYPE=ALLOWED_EXTENSIONS,
#     DROPZONE_MAX_FILE_SIZE=1000,
#     DROPZONE_INVALID_FILE_TYPE='Ce type de fichier n’est pas autorisé',
#     DROPZONE_TIMEOUT=300000 * 6,
#     DROPZONE_IN_FORM=True,
#     DROPZONE_UPLOAD_ON_CLICK=True,
#     DROPZONE_UPLOAD_ACTION='user_bp.handle_upload',  # URL or endpoint
#     DROPZONE_UPLOAD_BTN_ID='submit',
# )

photos = UploadSet('photos', IMAGES)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@user_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', title='Tableau de bord')


@user_bp.route('/new-file', methods=['GET', 'POST'])
@login_required
def new_file():
    simple_form = SingleFileForm()
    multi_form = NewFiles()
    if simple_form.is_submitted():
        filename = photos.save(simple_form.file.data)
        # n_file = File(name=filename, data=simple_form.file.data, owner=current_user.get_id())
        # db.session.add(n_file)
        # db.session.commit()
    # ...
    elif multi_form.validate_on_submit():
        pass
    # ...
    else:
        return render_template(
            'new-file.html',
            title='Nouveau fichier',
            single_file_form=simple_form,
            files_form=multi_form
        )


def encrypt_file(file, location):
    with open('file_key.key', 'rb') as file_key:
        stored_key = file_key.read()
    fernet = Fernet(stored_key)

    with open(location + '\\' + file.filename, 'rb') as file_to_encrypt:
        data_to_encrypt = file_to_encrypt.read()
    encrypted_data = fernet.encrypt(data_to_encrypt)

    with open(location + '\\' + file.filename, 'wb') as file_encrypted:
        file_encrypted.write(encrypted_data)


def decrypt_file():
    pass


def generate_fernet_key():
    k = Fernet.generate_key()
    # print(k)
    with open('file_key.key', 'wb') as new_file_key:
        new_file_key.write(k)
    return k


@user_bp.route('/upload', methods=['POST'])
@login_required
def handle_upload():
    simple_form = SingleFileForm()
    user_upload_folder = os.path.join('uploads', 'user_' + current_user.get_id())
    if request.method == 'POST':
        if not os.path.exists(user_upload_folder):
            os.makedirs(user_upload_folder)
        for key, file in request.files.items():
            file.filename = secure_filename(file.filename)
            if key.startswith('file') and allowed_file(file.filename):
                # print(file.filename+'yes')
                # encrypt
                file.save(os.path.join(user_upload_folder, file.filename))
                encrypt_file(file, user_upload_folder)
                #
                # n_file = File(name=file.filename, data=app.config['UPLOADED_PATH'],
                #              description=simple_form.description.data,
                #             owner=current_user.get_id())
                # db.session.add(n_file)
                # db.session.commit()
            elif not allowed_file(file.filename):
                print('file not allowed')
            else:
                print('nothing')

    return redirect(url_for('user_bp.new_file'))


@user_bp.route('import-folder', methods=['GET', 'POST'])
@login_required
def import_folder():
    return render_template('folder-import.html', title='Importer des Dossiers')


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
