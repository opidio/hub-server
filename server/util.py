from flask import jsonify
import random
import scrypt
import server


def invalid_parameter(param, message):
    return jsonify({
        'error': 'Invalid parameter',
        'parameter': param,
        'details': message
    }), 400


def invalid_request(message):
    return jsonify({
        'error': 'Invalid request',
        'details': message
    }), 400


def randstr(length):
    return ''.join(chr(random.randint(0, 255)) for i in range(length))


def hash_password(password):
    # Speed up the password hashing if in testing mode
    maxtime = 0.01 if server.app.config['TESTING'] else 1

    return scrypt.encrypt(randstr(64), password, maxtime=maxtime)


def verify_password(hashed_password, guessed_password):
    try:
        scrypt.decrypt(hashed_password, guessed_password, 1)
        return True
    except scrypt.error:
        return False


def get_video_url(video):
    return video.channel.url + ('/' if video.channel.url[-1] != '/' else '') + video.slug


class UnbufferedStream(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)
