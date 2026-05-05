from app import db
from datetime import datetime, timedelta
import secrets


class PasswordReset(db.Model):
    __tablename__ = 'password_resets'

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token      = db.Column(db.String(64), unique=True, nullable=False, index=True)
    usado      = db.Column(db.Boolean, default=False, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    criado_em  = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('User', backref='resets_senha')

    def __init__(self, user_id):
        self.user_id    = user_id
        self.token      = secrets.token_urlsafe(48)
        self.expires_at = datetime.utcnow() + timedelta(hours=1)

    @property
    def valido(self):
        return not self.usado and datetime.utcnow() < self.expires_at
