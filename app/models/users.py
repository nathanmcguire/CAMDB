from datetime import datetime
from hashlib import md5
from typing import List, Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
import platform

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(datetime.timezone.utc))

    posts: so.Mapped[List['Post']] = so.relationship('Post', back_populates='author')

    def __repr__(self):
        return '<User {}>'.format(self.username)

     
    def set_password(self, password: str) -> None:
        if platform.system() == 'Darwin':
            # macOS is missing scrypt, so we use pbkdf2:sha256
            self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        else:
            # Use scrypt or default for other systems
            self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'