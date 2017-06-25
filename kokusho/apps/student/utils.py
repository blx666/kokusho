import hashlib


def create_file_name(name):
    md5token = hashlib.md5()
    md5token.update(name.encode('utf-8'))
    file_name = md5token.hexdigest()
    return file_name