from app import db
from datetime import datetime

class Course(db.Model):
    """Modelo de Curso"""
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    nivel = db.Column(db.String(20), default='basico')  # basico, intermediario, avancado
    tempo_estimado = db.Column(db.Integer)  # em minutos
    autor = db.Column(db.String(120), nullable=False)
    imagem_url = db.Column(db.String(255), nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    aulas = db.relationship('Lesson', backref='curso', cascade='all, delete-orphan')
    progresso_usuarios = db.relationship('Progress', backref='curso', cascade='all, delete-orphan')
    
    def __init__(self, titulo, descricao, autor, nivel='basico', tempo_estimado=None, imagem_url=None, ativo=True):
        self.titulo = titulo
        self.descricao = descricao
        self.autor = autor
        self.nivel = nivel
        self.tempo_estimado = tempo_estimado
        self.imagem_url = imagem_url
        self.ativo = ativo
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'nivel': self.nivel,
            'tempo_estimado': self.tempo_estimado,
            'autor': self.autor,
            'ativo': self.ativo,
            'quantidade_aulas': len(self.aulas) if isinstance(self.aulas, list) else 0
        }
    
    def __repr__(self):
        return f'<Course {self.titulo}>'
