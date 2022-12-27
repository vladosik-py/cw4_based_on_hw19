import base64
import hashlib
import hmac

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def create(self, user_d):
        user_d["password"] = self.password_hash(user_d.get("password"))
        return self.dao.create(user_d)

    def update(self, user_d):
        user_d["password"] = self.password_hash(user_d.get("password"))
        self.dao.update(user_d)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)

    def password_hash(self, password):
        hashed_password = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return base64.b64encode(hashed_password)

    def compare_passwords(self, password_hash, other_password) -> bool:
        return hmac.compare_digest(
            base64.b64encode(password_hash),
            hashlib.pbkdf2_hmac(
                'sha256',
                other_password.encode("utf-8"),
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS
            )
        )