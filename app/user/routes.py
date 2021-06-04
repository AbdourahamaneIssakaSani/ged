import os.path

from flask import render_template, request, redirect, url_for, current_app as app
from flask_login import login_required, current_user
from flask_uploads import UploadSet, IMAGES

from .. import db
from ..models import File
from app.user import user_bp
from .forms import NewFile, NewFiles

basedir = os.path.abspath(os.path.dirname(__file__))
app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=10,
    DROPZONE_MAX_FILES=30,
    DROPZONE_IN_FORM=True,
    DROPZONE_UPLOAD_ON_CLICK=True,
    DROPZONE_UPLOAD_ACTION='user_bp.handle_upload',  # URL or endpoint
    DROPZONE_UPLOAD_BTN_ID='submit',
)

photos = UploadSet('photos', IMAGES)


@user_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', title='Tableau de bord')


@user_bp.route('/new-file', methods=['GET', 'POST'])
@login_required
def new_file():
    simple_form = NewFile()
    multi_form = NewFiles()
    if simple_form.is_submitted():
        filename = photos.save(simple_form.file.data)
        n_file = File(name=filename, data=simple_form.file.data, owner=current_user.get_id())
        print(n_file)
        db.session.add(n_file)
        db.session.commit()
    # ...
    elif multi_form.validate_on_submit():
        pass
    # ...
    else:
        return render_template(
            'new-file.html',
            title='Nouveau fichier',
            file_form=simple_form,
            files_form=multi_form
        )


@user_bp.route('/upload', methods=['POST'])
@login_required
def handle_upload():
    simple_form = NewFile()
    if simple_form.is_submitted():
        for key, file in request.files.items():
            if key.startswith('file'):
                file.save(os.path.join(app.config['UPLOADED_PATH'], file.filename))
                # print(file.save(os.path.join(app.config['UPLOADED_PATH'], file.filename)))
                n_file = File(name=file.filename, data=app.config['UPLOADED_PATH'], description=simple_form.description.data,
                              owner=current_user.get_id())
                print(simple_form.description)
                print(simple_form.description.data.encode('utf-8'))
                print(n_file.description)
                db.session.add(n_file)
                db.session.commit()
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
