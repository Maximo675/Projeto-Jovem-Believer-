from app import db
from datetime import datetime

class IAConversation(db.Model):
    """Modelo de Conversas com IA"""
    __tablename__ = 'ia_conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    pergunta = db.Column(db.Text, nullable=False)
    resposta = db.Column(db.Text, nullable=False)
    modelo_ia = db.Column(db.String(50), default='gpt-3.5-turbo')  # Modelo usado
    tokens_usados = db.Column(db.Integer, default=0)
    avaliacao = db.Column(db.Integer, nullable=True)  # 1-5 para feedback
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, usuario_id, pergunta, resposta, curso_id=None, modelo_ia='gpt-3.5-turbo', tokens_usados=0, avaliacao=None):
        self.usuario_id = usuario_id
        self.curso_id = curso_id
        self.pergunta = pergunta
        self.resposta = resposta
        self.modelo_ia = modelo_ia
        self.tokens_usados = tokens_usados
        self.avaliacao = avaliacao
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'curso_id': self.curso_id,
            'pergunta': self.pergunta,
            'resposta': self.resposta,
            'modelo_ia': self.modelo_ia,
            'avaliacao': self.avaliacao,
            'data_criacao': self.data_criacao.isoformat()
        }
    
    def __repr__(self):
        return f'<IAConversation Usuario {self.usuario_id}>'
