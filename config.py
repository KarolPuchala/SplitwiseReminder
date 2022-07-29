from os import getenv
from dotenv import load_dotenv

load_dotenv()

ssl_enable = getenv('SSL_ENABLE', False)
port = int(getenv('PORT'))
smtp_server = getenv('SMTP_SERVER')
username = getenv('MAIL_USERNAME')
password = getenv('MAIL_PASSWORD')
subject = getenv('SUBJECT')
sender = getenv('SENDER')
db_name = getenv('DB_NAME')

consumer_key = getenv('CONSUMER_KEY')
consumer_secret = getenv('CONSUMER_SECRET')
api_key = getenv('API_KEY')

