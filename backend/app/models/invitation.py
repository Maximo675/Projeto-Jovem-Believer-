from app import db
from datetime import datetime, timedelta
import uuid


class Invitation(db.Model):
    """Convite para ingresso na plataforma.

    Fluxo:
      super_admin cria hospital → cria admin do hospital
      admin cria convites para as enfermeiras do seu hospital
      Enfermeira recebe link → aceita via Microsoft ou email/senha
    """
    __tablename__ = 'invitations'

    id            = db.Column(db.Integer, primary_key=True)
    token         = db.Column(db.String(64), unique=True, nullable=False,
                              default=lambda: uuid.uuid4().hex)
    email         = db.Column(db.String(120), nullable=False, index=True)
    hospital_id   = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    funcao        = db.Column(db.String(50), nullable=False, default='usuario')
    usado         = db.Column(db.Boolean, default=False)
    expires_at    = db.Column(db.DateTime, nullable=False,
                              default=lambda: datetime.utcnow() + timedelta(days=7))
    criado_por_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    data_criacao  = db.Column(db.DateTime, default=datetime.utcnow)

    hospital   = db.relationship('Hospital', backref='convites')
    criado_por = db.relationship('User', foreign_keys=[criado_por_id])

    @property
    def expirado(self):
        return datetime.utcnow() > self.expires_at

    @property
    def valido(self):
        return not self.usado and not self.expirado

    def to_dict(self):
        return {
            'id':           self.id,
            'token':        self.token,
            'email':        self.email,
            'hospital_id':  self.hospital_id,
            'hospital':     self.hospital.nome if self.hospital else None,
            'funcao':       self.funcao,
            'usado':        self.usado,
            'expirado':     self.expirado,
            'expires_at':   self.expires_at.isoformat(),
            'data_criacao': self.data_criacao.isoformat(),
        }

    def __repr__(self):
        return f'<Invitation {self.email} → {self.hospital_id} [{self.funcao}]>'
