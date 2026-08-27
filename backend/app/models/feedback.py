"""
Modelo de Feedback da enfermeira/instrutor sobre um curso, com espaço para
resposta do super_admin. Mesma forma de dado de AdminNote
(backend/app/models/admin_note.py), só que na direção contrária
(usuario -> super_admin) e com os campos de resposta.
"""

from app import db
from datetime import datetime


class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)

    # 'sim' | 'parcial' | 'nao' — mantém os mesmos valores já usados em pages/course.html
    avaliacao_conteudo = db.Column(db.String(20), nullable=True)
    # 'facil' | 'medio' | 'dificil' — idem
    avaliacao_dificuldade = db.Column(db.String(20), nullable=True)
    comentario = db.Column(db.Text, nullable=True)

    resposta = db.Column(db.Text, nullable=True)
    respondido_por_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    respondido_em = db.Column(db.DateTime, nullable=True)

    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('User', foreign_keys=[usuario_id], lazy='joined')
    respondido_por = db.relationship('User', foreign_keys=[respondido_por_id], lazy='joined')
    curso = db.relationship('Course', lazy='joined')

    def to_dict(self, para_usuario=False):
        d = {
            'id': self.id,
            'curso_id': self.curso_id,
            'curso_titulo': self.curso.titulo if self.curso else None,
            'avaliacao_conteudo': self.avaliacao_conteudo,
            'avaliacao_dificuldade': self.avaliacao_dificuldade,
            'comentario': self.comentario,
            'resposta': self.resposta,
            'respondido_em': self.respondido_em.isoformat() if self.respondido_em else None,
            'data_criacao': self.data_criacao.isoformat(),
        }
        if not para_usuario:
            # visão do super_admin: inclui quem enviou e quem hospital
            d['usuario_id'] = self.usuario_id
            d['usuario_nome'] = self.usuario.nome if self.usuario else None
            d['hospital_id'] = self.usuario.hospital_id if self.usuario else None
            d['hospital_nome'] = (
                self.usuario.hospital.nome if self.usuario and self.usuario.hospital else None
            )
            d['respondido_por_nome'] = self.respondido_por.nome if self.respondido_por else None
        return d

    def __repr__(self):
        return f'<Feedback {self.id} usuario={self.usuario_id}>'
