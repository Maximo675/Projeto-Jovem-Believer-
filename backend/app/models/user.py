from app import db
from datetime import datetime
import bcrypt

class User(db.Model):
    """Modelo de Usuário"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    nome = db.Column(db.String(120), nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=True)
    funcao = db.Column(db.String(50), nullable=False, default='usuario')  # admin, instrutor, usuario
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    hospital = db.relationship('Hospital', backref='usuarios')
    progresso = db.relationship('Progress', backref='usuario', cascade='all, delete-orphan')
    conversas_ia = db.relationship('IAConversation', backref='usuario', cascade='all, delete-orphan')
    certificados = db.relationship('Certificate', backref='usuario', cascade='all, delete-orphan')
    
    def __init__(self, email, nome, senha, hospital_id=None, funcao='usuario', ativo=True):
        self.email = email
        self.nome = nome
        self.hospital_id = hospital_id
        self.funcao = funcao
        self.ativo = ativo
        self.set_password(senha)
    
    def set_password(self, senha):
        """Hashear e armazenar senha"""
        self.senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, senha):
        """Verificar senha"""
        return bcrypt.checkpw(senha.encode('utf-8'), self.senha_hash.encode('utf-8'))
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'email': self.email,
            'nome': self.nome,
            'hospital_id': self.hospital_id,
            'funcao': self.funcao,
            'ativo': self.ativo,
            'data_criacao': self.data_criacao.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.email}>'
