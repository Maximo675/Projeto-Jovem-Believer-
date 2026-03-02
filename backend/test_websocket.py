"""
Script de teste para WebSocket e atividades
Verifica se o servidor está funcionando corretamente
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = 'http://localhost:5001'
ACTIVITY_ID = 1
USER_ID = 1
LESSON_ID = 2

def test_activity_endpoints():
    """Testar endpoints HTTP da API de atividades"""
    
    print("\n" + "="*60)
    print("🧪 TESTE DE ENDPOINTS DE ATIVIDADES")
    print("="*60)
    
    # 1. Iniciar atividade
    print("\n1️⃣ POST /api/activities/<lesson_id>/start")
    response = requests.post(
        f'{BASE_URL}/api/activities/{LESSON_ID}/start',
        json={
            'activity_type': 'practice',
            'course_id': 1,
        },
        headers={'Authorization': 'Bearer fake_token'}  # Em produção, usar token real
    )
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        activity_id = response.json().get('activity_id')
        print(f"✅ Atividade criada: {activity_id}")
        
        # 2. Registrar tentativa
        print("\n2️⃣ POST /api/activities/<activity_id>/attempt")
        response = requests.post(
            f'{BASE_URL}/api/activities/{activity_id}/attempt',
            json={
                'responses': {'fase_1': True, 'fase_2': False},
                'score': 75,
                'time_taken': 120
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2)}")
        
        # 3. Completar atividade
        print("\n3️⃣ POST /api/activities/<activity_id>/complete")
        response = requests.post(
            f'{BASE_URL}/api/activities/{activity_id}/complete',
            json={
                'score': 85,
                'time_total': 600,
                'attempts': 1
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2)}")
        
        # 4. Obter detalhes
        print("\n4️⃣ GET /api/activities/<activity_id>/details")
        response = requests.get(f'{BASE_URL}/api/activities/{activity_id}/details')
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2)}")


def test_websocket_init():
    """Testar inicialização de WebSocket"""
    
    print("\n" + "="*60)
    print("🔌 TESTE DE INICIALIZAÇÃO WEBSOCKET")
    print("="*60)
    
    print("\n📡 POST /api/activities/ws-init/<activity_id>")
    response = requests.post(f'{BASE_URL}/api/activities/ws-init/1')
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ WebSocket pronto em: {data.get('ws_url')}")


def test_static_files():
    """Testar se arquivos estáticos são servidos corretamente"""
    
    print("\n" + "="*60)
    print("📁 TESTE DE ARQUIVOS ESTÁTICOS")
    print("="*60)
    
    files_to_test = [
        '/js/etan-websocket-client.js',
        '/js/iframe-bridge.js',
        '/pages/aula-com-atividades.html',
        '/activities/etan_protocol_simulator.html',
        '/activities/etan_special_cases.html',
        '/activities/etan_troubleshooting.html',
    ]
    
    for file_path in files_to_test:
        response = requests.head(f'{BASE_URL}{file_path}')
        status = "✅" if response.status_code == 200 else "❌"
        print(f"{status} {file_path}: {response.status_code}")


def test_database():
    """Testar se banco de dados está acessível"""
    
    print("\n" + "="*60)
    print("💾 TESTE DE BANCO DE DADOS")
    print("="*60)
    
    from app import create_app, db
    from app.models.activity import UserActivity, ActivityAttempt, ActivityBadge
    
    try:
        app = create_app()
        with app.app_context():
            # Contar registros
            user_activities = UserActivity.query.count()
            attempts = ActivityAttempt.query.count()
            badges = ActivityBadge.query.count()
            
            print(f"✅ Banco de dados acessível")
            print(f"   - user_activities: {user_activities} registros")
            print(f"   - activity_attempt: {attempts} registros")
            print(f"   - activity_badge: {badges} registros")
    except Exception as e:
        print(f"❌ Erro ao acessar banco: {e}")


def print_summary():
    """Imprimir resumo"""
    
    print("\n" + "="*60)
    print("📋 RESUMO DE TESTES")
    print("="*60)
    
    print("""
✅ Se todos os testes passaram:
   1. WebSocket está funcional
   2. API de atividades está respondendo
   3. Arquivos estáticos estão sendo servidos
   4. Banco de dados está acessível

📖 Próximos passos:
   1. Abra http://localhost:5001/pages/aula-com-atividades.html
   2. Abra console do navegador (F12)
   3. Complete uma atividade
   4. Verifique se eventos aparecem no log
   5. Abra o banco de dados sqlite para confirmar dados salvos

🔍 Debugging:
   - Verifique console do navegador para erros JavaScript
   - Verifique logs do servidor Flask para erros
   - Use F12 > Network para ver requisições
   - Use F12 > Console para ver mensagens WebSocket

💬 Commandos úteis:
   # Ver logs do servidor
   $ log tail backend.log
   
   # Inspeccionar WebSocket
   No console do navegador:
   > window.etanWebSocket.getConnectionInfo()
   > window.iframeBridge.getConnectionInfo()
   
   # Testar manualmente
   > window.etanWebSocket.joinActivity()
   > window.etanWebSocket.completeActivity(85, 600, 1, {})
    """)


if __name__ == '__main__':
    print("\n🚀 INICIANDO TESTES DE WEBSOCKET E ATIVIDADES\n")
    
    try:
        # Aguardar servidor estar pronto
        print("⏳ Aguardando servidor...", end='')
        for i in range(10):
            try:
                requests.get(f'{BASE_URL}/health')
                print(" ✅")
                break
            except:
                print(".", end='', flush=True)
                time.sleep(1)
        
        # Rodar testes
        test_static_files()
        test_database()
        test_websocket_init()
        test_activity_endpoints()
        print_summary()
        
    except Exception as e:
        print(f"\n❌ Erro durante testes: {e}")
        print("\n🔧 Solução: Verifique se o servidor Flask está rodando:")
        print("   $ cd backend && python run_verbose.py")
