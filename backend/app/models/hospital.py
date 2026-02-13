from app import db
from datetime import datetime

class Hospital(db.Model):
    """Modelo de Hospital"""
    __tablename__ = 'hospitals'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False, unique=True)
    estado = db.Column(db.String(2), nullable=False)  # Sigla do estado (SP, RJ, MG, etc)
    cidade = db.Column(db.String(120), nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    cnpj = db.Column(db.String(18), unique=True, nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento será definido apenas no User model - SEM backref aqui!
    
    def __init__(self, nome, estado, cidade, endereco, telefone, email, cnpj=None, ativo=True):
        self.nome = nome
        self.estado = estado
        self.cidade = cidade
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
        self.cnpj = cnpj
        self.ativo = ativo

    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'estado': self.estado,
            'cidade': self.cidade,
            'telefone': self.telefone,
            'email': self.email,
            'ativo': self.ativo
        }

    def __repr__(self):
        return f'<Hospital {self.nome}>'
