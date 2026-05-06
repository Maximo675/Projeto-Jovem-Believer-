from app import db
from datetime import datetime, timedelta
import secrets
import os


class PasswordReset(db.Model):
    __tablename__ = 'password_resets'

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token      = db.Column(db.String(64), unique=True, nullable=False, index=True)
    usado      = db.Column(db.Boolean, default=False, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    criado_em  = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('User', backref='resets_senha')

    def __init__(self, user_id, expiry_minutes=None):
        if expiry_minutes is None:
            expiry_minutes = int(os.getenv('RESET_TOKEN_EXPIRY_MINUTES', 60))
        self.user_id    = user_id
        self.token      = secrets.token_urlsafe(48)
        self.expires_at = datetime.utcnow() + timedelta(minutes=expiry_minutes)

    @property
    def valido(self):
        return not self.usado and datetime.utcnow() < self.expires_at

    @property
    def minutos_restantes(self):
        delta = self.expires_at - datetime.utcnow()
        return max(0, int(delta.total_seconds() / 60))
