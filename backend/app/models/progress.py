from app import db
from datetime import datetime

class Progress(db.Model):
    """Modelo de Progresso do Usuário"""
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    aula_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=True)
    percentual = db.Column(db.Integer, default=0)  # 0-100%
    concluido = db.Column(db.Boolean, default=False)
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_conclusao = db.Column(db.DateTime, nullable=True)
    tempo_gasto = db.Column(db.Integer, default=0)  # em segundos
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Índice único para evitar duplicatas
    __table_args__ = (db.UniqueConstraint('usuario_id', 'curso_id', name='_usuario_curso_uc'),)
    
    def __init__(self, usuario_id, curso_id, aula_id=None, percentual=0, concluido=False, tempo_gasto=0):
        self.usuario_id = usuario_id
        self.curso_id = curso_id
        self.aula_id = aula_id
        self.percentual = percentual
        self.concluido = concluido
        self.tempo_gasto = tempo_gasto
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'curso_id': self.curso_id,
            'percentual': self.percentual,
            'concluido': self.concluido,
            'data_inicio': self.data_inicio.isoformat(),
            'data_conclusao': self.data_conclusao.isoformat() if self.data_conclusao else None,
            'tempo_gasto': self.tempo_gasto
        }
    
    def __repr__(self):
        return f'<Progress Usuario {self.usuario_id} - Curso {self.curso_id}>'
