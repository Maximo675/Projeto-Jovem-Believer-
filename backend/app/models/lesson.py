from app import db
from datetime import datetime

class Lesson(db.Model):
    """Modelo de Aula"""
    __tablename__ = 'lessons'
    
    id = db.Column(db.Integer, primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    conteudo = db.Column(db.Text, nullable=False)  # HTML content
    ordem = db.Column(db.Integer, nullable=False)
    duracao = db.Column(db.Integer)  # em minutos
    video_url = db.Column(db.String(255), nullable=True)
    material_complementar = db.Column(db.Text, nullable=True)  # Links, arquivos, etc
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, curso_id, titulo, descricao, conteudo, ordem, duracao=None, video_url=None, material_complementar=None, ativo=True):
        self.curso_id = curso_id
        self.titulo = titulo
        self.descricao = descricao
        self.conteudo = conteudo
        self.ordem = ordem
        self.duracao = duracao
        self.video_url = video_url
        self.material_complementar = material_complementar
        self.ativo = ativo
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'curso_id': self.curso_id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'conteudo': self.conteudo,
            'ordem': self.ordem,
            'duracao': self.duracao,
            'video_url': self.video_url
        }
    
    def __repr__(self):
        return f'<Lesson {self.titulo}>'
