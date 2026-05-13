from app import db
from datetime import datetime


class AdminNote(db.Model):
    """Notas/feedback do administrador sobre uma enfermeira."""
    __tablename__ = 'admin_notes'

    id         = db.Column(db.Integer, primary_key=True)
    admin_id   = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    conteudo   = db.Column(db.Text, nullable=False)
    # 'elogio' | 'alerta' | 'observacao'
    tipo       = db.Column(db.String(20), nullable=False, default='observacao')
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    admin   = db.relationship('User', foreign_keys=[admin_id],   lazy='joined')
    usuario = db.relationship('User', foreign_keys=[usuario_id], lazy='joined')

    def to_dict(self):
        return {
            'id':          self.id,
            'admin_id':    self.admin_id,
            'admin_nome':  self.admin.nome if self.admin else None,
            'usuario_id':  self.usuario_id,
            'conteudo':    self.conteudo,
            'tipo':        self.tipo,
            'data_criacao': self.data_criacao.isoformat(),
        }

    def __repr__(self):
        return f'<AdminNote {self.tipo} by {self.admin_id} → {self.usuario_id}>'
