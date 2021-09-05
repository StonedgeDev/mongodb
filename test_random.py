# project/token.py

from flask import Flask

app = Flask(__name__)

from itsdangerous import URLSafeTimedSerializer

app.config['SECURITY_PASSWORD_SALT'] = 'adfadsfadf'
app.config['SECRET_KEY'] = 'ASDFADSF'

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email



print(confirm_token('Imp1c3R0b3RyeTEwMDZasdfasdAZ21haWwuY29tIg.YRZqiQ.vSHh2h3H_FbYPTvs6u-_kc3dyY0'))

