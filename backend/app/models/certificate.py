from app import db
from datetime import datetime
import uuid

class Certificate(db.Model):
    """Modelo de Certificado"""
    __tablename__ = 'certificates'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    numero_certificado = db.Column(db.String(50), unique=True, default=lambda: str(uuid.uuid4())[:8].upper())
    data_emissao = db.Column(db.DateTime, default=datetime.utcnow)
    validade = db.Column(db.Integer, nullable=True)  # em dias, None = sem validade
    arquivo_url = db.Column(db.String(255), nullable=True)
    
    def __init__(self, usuario_id, curso_id, validade=None, arquivo_url=None):
        self.usuario_id = usuario_id
        self.curso_id = curso_id
        self.validade = validade
        self.arquivo_url = arquivo_url
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'curso_id': self.curso_id,
            'numero_certificado': self.numero_certificado,
            'data_emissao': self.data_emissao.isoformat(),
            'validade': self.validade,
            'arquivo_url': self.arquivo_url
        }
    
    def __repr__(self):
        return f'<Certificate {self.numero_certificado}>'
