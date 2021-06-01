from flask_uploads import UploadSet, AllExcept, EXECUTABLES

allowed_files = UploadSet(AllExcept(EXECUTABLES))

# //TODO: Admin must allow all files extensions in the SETTINGS