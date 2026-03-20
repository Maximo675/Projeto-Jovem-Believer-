from flask import Blueprint, jsonify, request
from app import db
from app.models.ia_conversation import IAConversation
from app.models.user import User
from app.services.ai_service import AiService
import traceback
import io
import os

# Importações opcionais para OCR — requerem Tesseract instalado no sistema
try:
    import pytesseract
    from PIL import Image

    # Caminho padrão do Tesseract no Windows
    _tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(_tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = _tesseract_path

    OCR_DISPONIVEL = True
    print("[OCR] pytesseract e Pillow carregados com sucesso")
except ImportError:
    OCR_DISPONIVEL = False
    print("[OCR] pytesseract/Pillow não encontrados — endpoint de imagem desabilitado")

bp = Blueprint('ai', __name__, url_prefix='/api/ia')

ai_service = AiService()

@bp.route('/chat', methods=['POST'])
def chat_ia():
    """Endpoint de chat com IA (para dashboard)"""
    try:
        data = request.get_json()
        
        if not data or not data.get('mensagem'):
            return jsonify({'erro': 'Mensagem é obrigatória'}), 400
        
        mensagem = data['mensagem']
        
        # Consultar IA
        resposta, tokens = ai_service.responder_pergunta(mensagem)
        
        return jsonify({
            'mensagem': mensagem,
            'resposta': resposta,
            'tokens': tokens
        }), 200
        
    except Exception as e:
        traceback.print_exc()
        print(f"[AI ERROR] {str(e)}")
        return jsonify({'erro': f'Erro ao processar mensagem: {str(e)}'}), 500


@bp.route('/consult', methods=['POST'])
def consult_ia():
    """Consultar IA para dúvidas"""
    try:
        data = request.get_json()
        
        if not data or not data.get('pergunta'):
            return jsonify({'erro': 'Pergunta é obrigatória'}), 400
        
        usuario_id = data.get('usuario_id')
        curso_id = data.get('curso_id')
        pergunta = data['pergunta']
        
        # Validar usuário
        if usuario_id:
            usuario = User.query.get(usuario_id)
            if not usuario:
                return jsonify({'erro': 'Usuário não encontrado'}), 404
        
        # Consultar IA
        resposta, tokens = ai_service.responder_pergunta(pergunta, curso_id)
        
        # Salvar conversação
        conversa = IAConversation(
            usuario_id=usuario_id,
            curso_id=curso_id,
            pergunta=pergunta,
            resposta=resposta,
            tokens_usados=tokens
        )
        
        db.session.add(conversa)
        db.session.commit()
        
        return jsonify({
            'id': conversa.id,
            'pergunta': pergunta,
            'resposta': resposta,
            'tokens': tokens
        }), 200
        
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'erro': f'Erro ao consultao IA: {str(e)}'}), 500


_EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff'}
_TAMANHO_MAX_BYTES = 10 * 1024 * 1024  # 10 MB

def _extensao_permitida(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in _EXTENSOES_PERMITIDAS


# Mapeamento de padrões de erro detectáveis via OCR → instrução para a IA
_PADROES_ERRO_OCR = [
    # Hardware / dispositivo
    (('equipamento não encontrado', 'etan não encontrado', 'device not found',
      'dispositivo não encontrado', 'hardware não detectado', 'unable to find device'),
     'ERRO DETECTADO: Equipamento não encontrado. Explique como resolver o problema de conexão do ETAN.'),
    # USB
    (('code 43', 'código 43', 'unknown device', 'dispositivo usb desconhecido',
      'usb device not recognized', 'err_usb'),
     'ERRO DETECTADO: Falha de USB (Code 43 ou dispositivo desconhecido). Explique os passos para resolver.'),
    # Timeout / captura
    (('timeout', 'time out', 'tempo esgotado', 'operação expirou', 'captura expirou',
      'connection timeout', 'request timeout'),
     'ERRO DETECTADO: Timeout na captura ou conexão. Explique as causas e soluções.'),
    # Login / autenticação
    (('invalid credentials', 'credenciais inválidas', 'authentication failed',
      'falha na autenticação', 'usuário inválido', 'senha inválida', 'login failed'),
     'ERRO DETECTADO: Falha de autenticação/login. Oriente a enfermeira sobre como resolver o acesso.'),
    # SSL / certificado
    (('certificate error', 'ssl error', 'net::err_cert', 'conexão não segura',
      'certificado inválido', 'sua conexão não é privada'),
     'ERRO DETECTADO: Erro de certificado SSL. Explique as causas e como resolver.'),
    # Driver
    (('driver não encontrado', 'driver inválido', 'driver error', 'driver not found',
      'sem driver', 'driver corrompido'),
     'ERRO DETECTADO: Problema com driver do ETAN. Explique como reinstalar.'),
    # Sincronização
    (('sync error', 'erro de sincronização', 'upload failed', 'falha no upload',
      'dados não enviados', 'falha na sincronização'),
     'ERRO DETECTADO: Falha na sincronização de dados. Explique como recuperar a coleta.'),
    # NFIQ ruim
    (('nfiq 4', 'nfiq 5', 'qualidade insuficiente', 'quality insufficient', 'low quality'),
     'ERRO DETECTADO: NFIQ baixo (qualidade de digital insuficiente). Explique como melhorar.'),
    # Erros genéricos de sistema
    (('unhandled exception', 'fatal error', 'access denied', 'acesso negado',
      'null pointer', 'stacktrace', 'traceback', 'stack trace'),
     'ERRO DETECTADO: Erro de sistema (exceção/crash). Oriente sobre os próximos passos.'),
]


def _classificar_erro_ocr(texto: str) -> str:
    """
    Analisa o texto extraído por OCR e retorna uma instrução de contexto
    para a IA focar na solução correta. Retorna string vazia se nenhum padrão for detectado.
    """
    texto_lower = texto.lower()
    for padroes, instrucao in _PADROES_ERRO_OCR:
        if any(p in texto_lower for p in padroes):
            return instrucao
    return ''


@bp.route('/chat-imagem', methods=['POST'])
def chat_imagem():
    """
    Endpoint de chat com imagem (OCR + IA).
    Aceita multipart/form-data com:
      - imagem: arquivo de imagem (PNG, JPG, etc.)
      - mensagem: pergunta opcional da enfermeira (texto)
      - usuario_id: ID opcional do usuário
    """
    if not OCR_DISPONIVEL:
        return jsonify({
            'erro': 'OCR não disponível no servidor. Instale o Tesseract OCR e reinicie o backend.'
        }), 503

    if 'imagem' not in request.files:
        return jsonify({'erro': 'Nenhuma imagem enviada'}), 400

    arquivo = request.files['imagem']

    if arquivo.filename == '':
        return jsonify({'erro': 'Nome de arquivo vazio'}), 400

    if not _extensao_permitida(arquivo.filename):
        return jsonify({'erro': 'Formato de imagem não suportado. Use PNG, JPG, GIF, BMP ou WEBP.'}), 400

    # Ler em memória sem salvar no disco
    dados_imagem = arquivo.read()
    if len(dados_imagem) > _TAMANHO_MAX_BYTES:
        return jsonify({'erro': 'Imagem muito grande. Tamanho máximo permitido: 10 MB.'}), 413

    mensagem_usuario = (request.form.get('mensagem') or '').strip()
    usuario_id = request.form.get('usuario_id', type=int)

    try:
        imagem = Image.open(io.BytesIO(dados_imagem))
        # Converter para RGB para garantir compatibilidade com o Tesseract
        imagem = imagem.convert('RGB')
        texto_extraido = pytesseract.image_to_string(imagem, lang='por+eng').strip()
    except Exception as e:
        print(f"[OCR ERROR] Falha ao processar imagem: {e}")
        return jsonify({'erro': f'Erro ao processar imagem: {str(e)}'}), 500

    # Pré-classificar o erro detectado no print para dar contexto mais preciso à IA
    instrucao_erro = _classificar_erro_ocr(texto_extraido) if texto_extraido else ''

    # Montar pergunta contextualizada para a IA
    if texto_extraido:
        partes = []
        if instrucao_erro:
            partes.append(f"[{instrucao_erro}]")
        partes.append(f"[Texto extraído do print enviado pela enfermeira]\n{texto_extraido}")
        if mensagem_usuario:
            partes.append(f"[Pergunta da enfermeira]\n{mensagem_usuario}")
        else:
            partes.append(
                "Com base no erro mostrado no print, identifique o problema e explique "
                "como resolvê-lo de forma clara, objetiva e em português."
            )
        pergunta_final = "\n\n".join(partes)
    else:
        # OCR não encontrou texto — ainda assim tenta ajudar com a pergunta do usuário
        if mensagem_usuario:
            pergunta_final = (
                "[A enfermeira enviou um print da plataforma, mas não foi possível extrair texto dele.]\n\n"
                f"Pergunta da enfermeira: {mensagem_usuario}"
            )
        else:
            return jsonify({
                'texto_extraido': '',
                'resposta': (
                    'Recebi sua imagem, mas não consegui extrair texto dela. '
                    'Poderia descrever com palavras o que está acontecendo na tela? '
                    'Assim posso te ajudar melhor! 😊'
                ),
                'tokens': 0
            }), 200

    resposta, tokens = ai_service.responder_pergunta(pergunta_final)

    # Salvar no histórico se houver usuário identificado
    if usuario_id:
        try:
            resumo_pergunta = mensagem_usuario or f"[Print enviado] {texto_extraido[:120]}..."
            conversa = IAConversation(
                usuario_id=usuario_id,
                pergunta=resumo_pergunta,
                resposta=resposta,
                tokens_usados=tokens
            )
            db.session.add(conversa)
            db.session.commit()
        except Exception:
            db.session.rollback()

    return jsonify({
        'texto_extraido': texto_extraido,
        'resposta': resposta,
        'tokens': tokens
    }), 200


@bp.route('/historico/<int:user_id>', methods=['GET'])
def get_historico(user_id):
    """Obter histórico de conversas"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        conversas = IAConversation.query.filter_by(usuario_id=user_id).paginate(page=page, per_page=per_page)
        
        return jsonify({
            'total': conversas.total,
            'paginas': conversas.pages,
            'conversas': [c.to_dict() for c in conversas.items]
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@bp.route('/avaliar/<int:conversa_id>', methods=['PUT'])
def avaliar_resposta(conversa_id):
    """Avaliar resposta da IA"""
    try:
        conversa = IAConversation.query.get(conversa_id)
        
        if not conversa:
            return jsonify({'erro': 'Conversa não encontrada'}), 404
        
        data = request.get_json()
        if 'avaliacao' not in data:
            return jsonify({'erro': 'Avaliação é obrigatória'}), 400
        
        conversa.avaliacao = data['avaliacao']
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Avaliação registrada',
            'conversa': conversa.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500
