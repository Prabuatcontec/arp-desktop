class Config(object):
    DATABASE_CONFIG = {
        'server': 'crs-dev.cnvayknczt9m.us-east-1.rds.amazonaws.com',
        'user': 'VulcanWebUser',
        'password': 'Vulcan123',
        'name': 'Automation',
    }
    UPLOAD_FOLDER = './static/uploads/'
    API_URL = 'http://localhost:5000/api/'
    API_USER_URL = 'http://api.vulcan.contecprod.com/api/'
    REPO_PATH = 'https://github.com/Prabuatcontec/ocr-receiving'
    DEEPBLU_URL = 'https://deepbluapi.gocontec.com'
    DEEPBLU_KEY = 'QVVUT1JFQ0VJVkU6YXV0b0AxMjM='
    CAMERA_NO = 0
    CAMERA_WIDTH = 3000
    CAMERA_HEIGHT = 1900
    #CAMERA_WIDTH = 2500
    #CAMERA_HEIGHT = 1900
