import os
import logging

LOG_LEVEL = logging.DEBUG
PRESERVE_CONTEXT_ON_EXCEPTION = True
DEBUG = False

SESSION_COOKIE_SAMESITE = 'strict'
SESSION_COOKIE_PATH = '/'
SESSION_KEY_PREFIX = "hello"
SESSION_COOKIE_NAME = "FinanceHub"
# SESSION_COOKIE_SECURE = True
# REMEMBER_COOKIE_SECURE = True

ROOT_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), '..', '..'))
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
DOC_DIR = os.path.join(ROOT_DIR, 'claim_docs')
TEMP_DIR = os.path.join(ROOT_DIR, 'temp')
DATA_DIR = os.path.join(ROOT_DIR, "portal")

DIRECTORIES = [LOG_DIR, DOC_DIR, TEMP_DIR]
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'rar', '7z'}
SECRET_KEY = "Kc5c3zTk'-3<&BdL:P92O{_(:-NkY+"

MONGO_URI = "mongodb+srv://root:root12345@spookyfinancehubv2.ia1zt.mongodb.net/?retryWrites=true&w=majority&appName=SpookyFinanceHubV2"
URL_MAIN="https://spookyspender-402086265060.us-central1.run.app"

PROPAGATE_EXCEPTIONS = True

CORS_HEADERS = [
    'Content-Type',
    'Authorization'
]

CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1",
    "https://127.0.0.1",
    "http://127.0.0.1:5000",
    "https://127.0.0.1:5000",
    "http://127.0.0.1:4200",
    "https://127.0.0.1:4200",
    "http://localhost",
    "https://localhost",
    "http://localhost:5000",
    "https://localhost:5000",
    "http://localhost:4200",
    "https://localhost:4200",
]
