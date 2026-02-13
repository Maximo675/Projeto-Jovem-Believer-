"""
Testes da API de Autenticação
"""

import pytest
import json
from app import create_app, db
from app.models.user import User
from app.models.hospital import Hospital

@pytest.fixture
def app():
    """Cria aplicação para testes"""
    app = create_app()
    
    with app.app_context():
        # Tabelas já foram criadas no DBeaver
        # db.create_all()
        
        # Criar hospital de teste
        hospital = Hospital(
            nome="Hospital Teste",
            estado="SP",
            cidade="São Paulo",
            endereco="Rua Test",
            telefone="1234567890",
            email="hospital@test.com"
        )
        db.session.add(hospital)
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente para testes"""
    return app.test_client()

def test_registro_usuario(client):
    """Testa registro de novo usuário"""
    response = client.post('/api/auth/register', 
        json={
            'email': 'teste@hospital.com',
            'nome': 'João Teste',
            'senha': 'senha123',
            'hospital_id': 1
        }
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'usuario' in data
    assert data['usuario']['email'] == 'teste@hospital.com'

def test_login_usuario(client, app):
    """Testa login de usuário"""
    # Primeiro registra um usuário
    with app.app_context():
        usuario = User(
            email='teste@hospital.com',
            nome='João Teste',
            senha='senha123',
            hospital_id=1,
            funcao='usuario'
        )
        usuario.set_password('senha123')
        db.session.add(usuario)
        db.session.commit()
    
    # Tenta fazer login
    response = client.post('/api/auth/login',
        json={
            'email': 'teste@hospital.com',
            'senha': 'senha123'
        }
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data
    assert 'usuario' in data

def test_login_email_invalido(client):
    """Testa login com email inválido"""
    response = client.post('/api/auth/login',
        json={
            'email': 'invalido@test.com',
            'senha': 'senha123'
        }
    )
    
    assert response.status_code == 401

def test_email_duplicado(client):
    """Testa registro com email duplicado"""
    # Primeiro registro
    client.post('/api/auth/register',
        json={
            'email': 'duplicado@hospital.com',
            'nome': 'Primeiro',
            'senha': 'senha123',
            'hospital_id': 1
        }
    )
    
    # Segundo registro com mesmo email
    response = client.post('/api/auth/register',
        json={
            'email': 'duplicado@hospital.com',
            'nome': 'Segundo',
            'senha': 'senha123',
            'hospital_id': 1
        }
    )
    
    assert response.status_code == 400
