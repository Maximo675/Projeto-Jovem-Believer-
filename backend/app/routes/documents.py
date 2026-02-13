from flask import Blueprint, jsonify, request, send_file
from app.services.document_service import DocumentService, KnowledgeBaseManager
import os

bp = Blueprint('documents', __name__, url_prefix='/api/documents')

@bp.route('', methods=['GET'])
def list_documents():
    """Listar todos os documentos da knowledge base"""
    try:
        documentos = DocumentService.listar_documentos()
        
        return jsonify({
            'total': len(documentos),
            'documentos': documentos
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@bp.route('/<nome_arquivo>', methods=['GET'])
def get_document(nome_arquivo):
    """Obter conteúdo de um documento específico"""
    try:
        documento = DocumentService.obter_documento(nome_arquivo + '.docx')
        
        return jsonify(documento), 200
        
    except FileNotFoundError:
        return jsonify({'erro': 'Documento não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@bp.route('/<nome_arquivo>/download', methods=['GET'])
def download_document(nome_arquivo):
    """Download de um documento específico"""
    try:
        from pathlib import Path
        
        knowledge_base_dir = Path(__file__).parent.parent.parent / 'assets' / 'documents'
        caminho = knowledge_base_dir / f"{nome_arquivo}.docx"
        
        if not caminho.exists():
            return jsonify({'erro': 'Documento não encontrado'}), 404
        
        return send_file(
            str(caminho),
            as_attachment=True,
            download_name=f"{nome_arquivo}.docx"
        ), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@bp.route('/indice', methods=['GET'])
def get_knowledge_index():
    """Obter índice completo da base de conhecimento"""
    try:
        indice = KnowledgeBaseManager.gerar_indice_conhecimento()
        
        return jsonify(indice), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@bp.route('/sincronizar', methods=['POST'])
def sync_documents():
    """Sincronizar documentos (apenas admin)"""
    try:
        resultado = KnowledgeBaseManager.sincronizar_documentos()
        
        return jsonify(resultado), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
