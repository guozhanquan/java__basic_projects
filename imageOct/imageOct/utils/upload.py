from flask import current_app


def file_check(filename):

    return '.' in filename and filename.split('.')[-1] in current_app.config['ALLOWED_FILE']
