# -*- coding: utf-8 -*-
"""
Proxy completo para infant.akiyama.com.br + APIs Akiyama + OpenBio local

Estratégia:
- /infant/<path>        → proxy de https://infant.akiyama.com.br
                          Injeta script que: mocka auth, redireciona APIs externas
- /openbio/<path>       → proxy de http://localhost:5000 (server-side, sem CORS)
- /akiyama-api/<path>   → proxy de APIs externas da Akiyama (api-management, api-enroll)
                          Retorna mocks quando 401 para evitar redirect de login

UUID do cliente local (C:\Openbio\customer.ini):
  uuid = 05e082fe-6062-43ff-a093-b14b13562b28
"""

from flask import Blueprint, request, Response
import requests as req_lib
import urllib3
import json
import socket
import os
import xml.etree.ElementTree as ET

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

bp = Blueprint('infant_proxy', __name__)

INFANT_ORIGIN    = 'https://infant.akiyama.com.br'
OPENBIO_ORIGIN   = 'http://localhost:5000'
FLASK_BASE       = 'http://127.0.0.1:5001'
CUSTOMER_UUID    = '05e082fe-6062-43ff-a093-b14b13562b28'

EXCLUDED_REQ_HEADERS = {'host', 'content-length', 'transfer-encoding', 'connection'}
EXCLUDED_RES_HEADERS = {
    'content-encoding', 'content-length', 'transfer-encoding',
    'connection', 'keep-alive',
    # ← estes dois são os culpados pelo bloqueio do iframe
    'x-frame-options', 'content-security-policy',
    'x-content-type-options',
}

# ─────────────────────────────────────────────────────────────
# Mock responses para APIs externas que exigem auth
# ─────────────────────────────────────────────────────────────

MOCK_ACCOUNT_USER = {
    "id": CUSTOMER_UUID,
    "customerId": CUSTOMER_UUID,
    "accountId": CUSTOMER_UUID,
    "name": "Local ETAN User",
    "email": "etan@local.dev",
    "role": "ADMIN",
    "status": "ACTIVE",
    "authenticated": True,
    "customerTheme": {
        "primaryColor": "#667eea",
        "secondaryColor": "#764ba2",
        "logoUrl": None,
        "name": "Default"
    },
    "permissions": ["READ", "WRITE", "BIOMETRIC_CAPTURE", "ADMIN"],
    "account": {
        "id": CUSTOMER_UUID,
        "customerId": CUSTOMER_UUID,
        "name": "Alura Jovem Believer",
        "uuid": CUSTOMER_UUID,
        "status": "ACTIVE",
        "subscriptionStatus": "ACTIVE",
        "customerTheme": {
            "primaryColor": "#667eea",
            "secondaryColor": "#764ba2",
            "logoUrl": None,
            "name": "Default"
        }
    },
    "customer": {
        "id": CUSTOMER_UUID,
        "name": "Alura Jovem Believer",
        "uuid": CUSTOMER_UUID,
        "status": "ACTIVE",
        "customerTheme": {
            "primaryColor": "#667eea",
            "secondaryColor": "#764ba2",
            "logoUrl": None,
            "name": "Default"
        }
    }
}

MOCK_FORM_TYPE = {
    "id": 1,
    "formTypeId": 2,
    "service": "infant",
    "status": "ACTIVE",
    "customerId": CUSTOMER_UUID,
    "name": "Infant Capture Form"
}

MOCK_DYNAMIC_FORMS = {
    "content": [],
    "totalElements": 0,
    "formTypeId": 2,
    "customerId": CUSTOMER_UUID,
    "page": {"size": 10, "number": 0, "totalElements": 0, "totalPages": 0}
}

def _mock_json(data, status=200):
    return Response(
        json.dumps(data),
        status=status,
        headers={
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        }
    )

# ─────────────────────────────────────────────────────────────
# Script injetado no <head> do HTML do Infant
# ─────────────────────────────────────────────────────────────

INTERCEPTOR_SCRIPT = f"""<script>
(function() {{
    var BASE = '{FLASK_BASE}';
    var CUSTOMER_ID = '{CUSTOMER_UUID}';
    var ETAN_SDK = '__ETAN_SDK__';  // injetado dinamicamente pelo proxy — não edite

    // 0. Remover banner "SISTEMA DESATUALIZADO" que bloqueia a captura
    function removeBannerDesatualizado() {{
        var banners = document.querySelectorAll(
            '[class*="alert"], [class*="Alert"], [class*="warning"], [class*="Warning"], ' +
            '[class*="update"], [class*="Update"], [class*="outdated"], [class*="banner"]'
        );
        banners.forEach(function(el) {{
            var txt = el.textContent || '';
            if (txt.indexOf('DESATUALIZADO') > -1 || txt.indexOf('desatualizado') > -1 ||
                txt.indexOf('Atualiz') > -1 || txt.indexOf('atualiz') > -1 ||
                txt.indexOf('nova vers') > -1 || txt.indexOf('Nova vers') > -1) {{
                el.style.display = 'none';
                el.remove();
                console.log('[Proxy] Banner desatualizado removido');
            }}
        }});
    }}
    // Verificar a cada 300ms por 30 segundos (cobre render SPA + demora de update check)
    var _bannerInterval = setInterval(removeBannerDesatualizado, 300);
    setTimeout(function() {{ clearInterval(_bannerInterval); }}, 30000);
    // Também observar mutações no DOM
    if (window.MutationObserver) {{
        var _obs = new MutationObserver(removeBannerDesatualizado);
        document.addEventListener('DOMContentLoaded', function() {{
            _obs.observe(document.body || document.documentElement,
                         {{ childList: true, subtree: true }});
        }});
    }}

    // 1. Injetar customer UUID + SDK version no localStorage ANTES de qualquer JS do infant
    try {{
        localStorage.setItem('customerId', CUSTOMER_ID);
        localStorage.setItem('customer_uuid', CUSTOMER_ID);
        localStorage.setItem('__customer_id__', CUSTOMER_ID);
        // Forçar SDK version para 0.3.0.0 no localStorage
        localStorage.setItem('infantSdkVersion', ETAN_SDK);
        localStorage.setItem('sdk_version', ETAN_SDK);
        localStorage.setItem('device_sdk', ETAN_SDK);
    }} catch(e) {{}}

    // 2. Função para redirecionar URLs
    function patchUrl(url) {{
        if (typeof url !== 'string') return url;
        // OpenBio local
        if (url.indexOf('localhost:5000') > -1)
            return url.replace(/http:\\/\\/localhost:5000/, BASE + '/openbio');
        if (url.indexOf('127.0.0.1:5000') > -1)
            return url.replace(/http:\\/\\/127\\.0\\.0\\.1:5000/, BASE + '/openbio');
        // APIs externas Akiyama → nosso proxy Flask
        if (url.indexOf('api-management.akiyama.com.br') > -1)
            return url.replace(/https:\\/\\/api-management\\.akiyama\\.com\\.br/, BASE + '/akiyama-api/management');
        if (url.indexOf('api-enroll.akiyama.com.br') > -1)
            return url.replace(/https:\\/\\/api-enroll\\.akiyama\\.com\\.br/, BASE + '/akiyama-api/enroll');
        return url;
    }}

    // 3. Patch XMLHttpRequest
    var _open = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function(method, url, async, user, pass) {{
        var patched = patchUrl(url);
        if (patched !== url) console.log('[Proxy] XHR:', url.substring(0,60), '→', patched.substring(0,60));
        return _open.call(this, method, patched, async, user, pass);
    }};

    // 4. Patch fetch
    var _fetch = window.fetch;
    window.fetch = function(resource, config) {{
        if (typeof resource === 'string') {{
            var patched = patchUrl(resource);
            if (patched !== resource) console.log('[Proxy] fetch:', resource.substring(0,60), '→', patched.substring(0,60));
            resource = patched;
        }} else if (resource && resource.url) {{
            resource = new Request(patchUrl(resource.url), resource);
        }}
        return _fetch.call(this, resource, config);
    }};

    // 5. Patch WebSocket: redirecionar urls e interceptar mensagens de licença
    var _WS = window.WebSocket;

    function patchWsUrl(url) {{
        if (typeof url !== 'string') return url;
        // Redirecionar porta Flask (5001) → OpenBio (5000)
        if (url.indexOf('localhost:5001') > -1 || url.indexOf('127.0.0.1:5001') > -1)
            url = url.replace(/localhost:5001/, 'localhost:5000').replace(/127\.0\.0\.1:5001/, 'localhost:5000');
        // Updater WS sem path específico → /interface para evitar loop de erros
        if ((url === 'ws://localhost:5000' || url === 'ws://localhost:5000/' ||
             url === 'ws://127.0.0.1:5000' || url === 'ws://127.0.0.1:5000/') ||
            (url.indexOf('localhost:5000') > -1 && url.indexOf('/device') === -1 && url.indexOf('/interface') === -1)) {{
            console.log('[Proxy] WS updater sem path → redirecionando para /interface');
            return 'ws://localhost:5000/interface';
        }}
        // /device agora ACEITA conexão (customerId configurado corretamente)
        // Código 10 (INSTALLATION_LIMIT_REACHED) ao invés de 11 = WS fica aberto
        // Deixamos /device como está e interceptamos license-validation-error em patchWsMessage
        if (url.indexOf('/device') > -1) {{
            console.log('[Proxy] WS /device → conectando ao device real (license bypass via intercept)');
        }}
        return url;
    }}

    function patchWsMessage(data) {{
        if (typeof data !== 'string') return data;
        try {{
            var msg = JSON.parse(data);
            var modified = false;

            // ── 1. Interceptar erros de licença → BLOQUEAR (SPA já recebeu resposta sintética via send())
            if (msg.status === 'license-validation-error' ||
                msg.status === 'license-error' ||
                msg.status === 'INSTALLATION_LIMIT_REACHED' ||
                (msg.code && (msg.code === 10 || msg.code === 11) && msg.message && msg.message.indexOf('LICENSE') > -1)) {{
                console.log('[Proxy] WS: license-error bloqueado (já injetado synthetic response)');
                return null; // SPA não vê este erro
            }}

            // ── 2. Interceptar license-validation com valid:false ────────────────
            if (msg.action === 'license-validation' && msg.valid === false) {{
                console.log('[Proxy] WS: license-validation false → true');
                return JSON.stringify({{
                    action: 'license-validation',
                    valid: true,
                    status: 'license-validation-success',
                    message: 'OK'
                }});
            }}

            // ── 3. Patch campos de licença em mensagens genéricas ────────────────
            // ── 4. Patch server.isConnected → sempre true ────────────────────────────
            // A SPA faz destructure de server.remoteApi sem null-check —
            // se `server` estiver ausente na mensagem real do OpenBio → TypeError crash.
            // Portanto, sempre injetamos o campo se ele não vier na mensagem.
            if (!msg.server) {{
                msg.server = {{ remoteApi: false, isConnected: true, enabled: true }};
                modified = true;
            }} else {{
                if (msg.server.isConnected === false) {{ msg.server.isConnected = true; modified = true; }}
                if (msg.server.enabled === false)     {{ msg.server.enabled     = true; modified = true; }}
                if (msg.server.remoteApi !== false)   {{ msg.server.remoteApi   = false; modified = true; }}
            }}

            // ── 4b. Interceptar ações de desconexão e de update ──────────────────────
            if (msg.action) {{
                var a = msg.action.toLowerCase();
                if (a.indexOf('disconnect') > -1 || a.indexOf('session-expired') > -1 ||
                    a.indexOf('session-invalid') > -1 || a.indexOf('force-reload') > -1) {{
                    console.log('[Proxy] WS: interceptado action de desconexão →', msg.action, '— BLOQUEADO');
                    return null;
                }}
                // Bloquear mensagens de update/sistema desatualizado
                // NOTA: NÃO bloquear 'installer-localization' que carrega traduções da SPA (SDK 0.3.0.0+)
                if (a.indexOf('update-available') > -1 || a.indexOf('new-version') > -1 ||
                    a.indexOf('system-update') > -1 || a.indexOf('device-outdated') > -1 ||
                    (a.indexOf('installer-') > -1 && a.indexOf('localiz') === -1 &&
                     a.indexOf('translat') === -1 && a.indexOf('i18n') === -1)) {{
                    console.log('[Proxy] WS: mensagem de update BLOQUEADA →', msg.action);
                    return null;
                }}
            }}

            // ── 4c. Patch deviceStatuses: garantir infant em TODAS as mensagens ─────────
            if (msg.deviceStatuses) {{
                // SDK 0.3.0.0: OpenBio pode não incluir infant no status da interface
                // → sempre injetar infant como conectado se ausente
                if (!msg.deviceStatuses.infant) {{
                    msg.deviceStatuses.infant = {{
                        initialized: true, enabled: true, sdkVersion: ETAN_SDK,
                        info: 'EtanV2', connected: true, loaded: true, ready: true,
                        loading: false, status: 'connected', captureEnabled: true,
                        canUseInfant: true, licenseValid: true, hasUpdate: false,
                        device: {{ id: 'EtanV2', name: 'ETAN V2', type: 'infant',
                                   status: 'connected', initialized: true, loaded: true,
                                   ready: true, captureEnabled: true, sdkVersion: ETAN_SDK }}
                    }};
                    modified = true;
                    console.log('[Proxy] WS: infant injetado (SDK detectado=' + ETAN_SDK + ')');
                }} else {{
                    var inf = msg.deviceStatuses.infant;
                    if (!inf.initialized)      {{ inf.initialized    = true;  modified = true; }}
                    if (!inf.connected)        {{ inf.connected      = true;  modified = true; }}
                    if (!inf.loaded)           {{ inf.loaded         = true;  modified = true; }}
                    if (!inf.ready)            {{ inf.ready          = true;  modified = true; }}
                    if (inf.loading !== false)  {{ inf.loading        = false; modified = true; }}
                    if (!inf.captureEnabled)   {{ inf.captureEnabled  = true;  modified = true; }}
                    if (!inf.canUseInfant)     {{ inf.canUseInfant    = true;  modified = true; }}
                    // Normalizar qualquer versão do SDK diferente da detectada → ETAN_SDK (agnóstico de versão)
                    if (inf.sdkVersion && inf.sdkVersion !== ETAN_SDK) {{
                        inf.sdkVersion = ETAN_SDK; modified = true;
                    }}
                    if (!inf.status || inf.status === 'loading' || inf.status === 'disconnected') {{
                        inf.status = 'connected'; modified = true;
                    }}
                    if (!inf.device && inf.info) {{
                        inf.device = {{ id: inf.info, name: inf.info, status: 'connected',
                                        initialized: true, loaded: true, ready: true,
                                        sdkVersion: ETAN_SDK }};
                        modified = true;
                    }}
                }}
                // Bloquear flags de update no device modal (evita banner SISTEMA DESATUALIZADO)
                if (msg.deviceStatuses.modal) {{
                    var m = msg.deviceStatuses.modal;
                    if (m.hasUpdate)       {{ m.hasUpdate        = false; modified = true; }}
                    if (m.updateAvailable) {{ m.updateAvailable  = false; modified = true; }}
                    if (m.updateRequired)  {{ m.updateRequired   = false; modified = true; }}
                    if (m.newVersion)      {{ m.newVersion       = null;  modified = true; }}
                }}
            }}

            var licenseFields = ['licensed','isLicensed','hasLicense','infantLicense',
                                 'infantEnabled','hasInfant','licenseValid','license_valid',
                                 'module_enabled','moduleEnabled'];
            function deepPatch(obj) {{
                if (!obj || typeof obj !== 'object') return;
                for (var k in obj) {{
                    if (!obj.hasOwnProperty(k)) continue;
                    if (licenseFields.indexOf(k) > -1 && obj[k] === false) {{
                        console.log('[Proxy] WS patch campo:', k, '→ true'); obj[k] = true; modified = true;
                    }}
                    if ((k==='licenseStatus'||k==='license_status') && obj[k]!=='ACTIVE') {{
                        obj[k]='ACTIVE'; modified=true;
                    }}
                    if (k==='enrollmentValidations' && obj[k] && obj[k].infant===false) {{
                        obj[k].infant=true; modified=true;
                    }}
                    if (k==='modules' && Array.isArray(obj[k])) {{
                        obj[k].forEach(function(m) {{
                            if (m && (m.name==='infant'||m.module==='infant')) {{
                                if (m.enabled===false){{m.enabled=true;modified=true;}}
                                if (m.licensed===false){{m.licensed=true;modified=true;}}
                                if (m.status==='INACTIVE'){{m.status='ACTIVE';modified=true;}}
                            }}
                        }});
                    }}
                    if (obj[k] && typeof obj[k]==='object') deepPatch(obj[k]);
                }}
            }}
            deepPatch(msg);
            if (modified) {{
                console.log('[Proxy] WS msg patchada:', JSON.stringify(msg).substring(0,200));
                return JSON.stringify(msg);
            }}
        }} catch(e) {{}}
        return data;
    }}

    // ── Estado completo dos devices (infant=ETAN pronto) ────────────────────────
    var INFANT_READY = {{
        server: {{ remoteApi: false, isConnected: true, enabled: true }},
        deviceStatuses: {{
            face:      {{ initialized: false, enabled: true,  sdkVersion: '1.8.1.4' }},
            signature: {{ initialized: true,  info: 'ESP_560', enabled: true, sdkVersion: '1.8.0.3' }},
            modal:     {{ initialized: false, enabled: true, sdkVersion: '0.3.3.15' }},
            infant: {{
                initialized: true, enabled: true, sdkVersion: ETAN_SDK,
                info: 'EtanV2', connected: true, loaded: true, ready: true,
                loading: false, status: 'connected', captureEnabled: true,
                canUseInfant: true, licenseValid: true, hasUpdate: false,
                device: {{
                    id: 'EtanV2', name: 'ETAN V2', type: 'infant',
                    status: 'connected', initialized: true, loaded: true,
                    ready: true, captureEnabled: true, sdkVersion: ETAN_SDK
                }}
            }}
        }}
    }};

    window.WebSocket = function(url, protocols) {{
        var pUrl = patchWsUrl(url);
        if (pUrl !== url) console.log('[Proxy] WS URL:', url, '→', pUrl);
        var ws = protocols !== undefined ? new _WS(pUrl, protocols) : new _WS(pUrl);
        // isDevice baseia-se na URL ORIGINAL (pUrl já pode ser /interface por redirect)
        var isDevice = url.indexOf('/device') > -1;

        function inject(payload, delay) {{
            setTimeout(function() {{
                ws.dispatchEvent(new MessageEvent('message', {{data: JSON.stringify(payload)}}));
            }}, delay || 50);
        }}

        function injectDeviceReady() {{
            if (!isDevice) return;
            inject(INFANT_READY, 400);
            inject(INFANT_READY, 900);
        }}

        // ── Estado interno do WS real (não visível ao SPA) ─────────────────────
        var _isDeviceWsClosed = false;
        var _realWsOpened = false;
        var _keepAliveInterval = null;

        var _wsSend = ws.send.bind(ws);
        ws.send = function(data) {{
            if (typeof data === 'string' && data.length < 800)
                console.log('[Proxy] WS send (' + (isDevice?'DEV':'IFACE') + '):', data.substring(0,200));

            // ── Interface WS: interceptar ações que causam chamadas remotas ──────
            if (!isDevice) {{
                try {{
                    var ifMsg = JSON.parse(data);
                    var ifAct = ifMsg.action;
                    if (ifAct === 'store-customer-id') {{
                        console.log('[Proxy] IFACE intercept store-customer-id → inject success (sem pass-through)');
                        inject({{
                            action: 'store-customer-id-response',
                            status: 'success',
                            serviceId: ifMsg.data && ifMsg.data.serviceId || 1
                        }});
                        return; // NÃO repassar ao OpenBio: evita chamada à API Akiyama que gera "Error sending customer app informations"
                    }}
                    if (ifAct === 'store-service-id' || ifAct === 'set-service') {{
                        inject({{ action: ifAct + '-response', status: 'success' }});
                        return _wsSend(data);
                    }}
                    // get-hardware-info também chega na Interface WS
                    if (ifAct === 'get-hardware-info') {{
                        inject({{ action:'hardware-info', status:'success',
                                   hardware:{{ processor:'Intel Core i7', ram:'16GB',
                                              disk:'512GB SSD', network:'Ethernet' }},
                                   server: INFANT_READY.server }});
                        return;
                    }}
                }} catch(e) {{}}
                return _wsSend(data);
            }}

            // ── Device WS: interceptar e responder sinteticamente ────────────────
            try {{
                var sent = JSON.parse(data);
                var act = sent.action;

                if (act === 'clear-session') {{
                    inject({{ action: 'clear-session-response', status: 'success' }});
                    return;
                }}
                if (act === 'get-hardware-info') {{
                    inject({{ action:'hardware-info', status:'success',
                               hardware:{{ processor:'Intel Core i7', ram:'16GB',
                                          disk:'512GB SSD', network:'Ethernet' }},
                               server: INFANT_READY.server }});
                    return;
                }}
                if (act === 'store-customer-id') {{
                    inject({{ action:'store-customer-id-response', status:'success' }});
                    return; // NÃO repassar ao OpenBio: evita chamada à API Akiyama que gera "Error sending customer app informations"
                }}
                if (act === 'validate-license') {{
                    console.log('[Proxy] DEV intercept validate-license → inject success');
                    inject(Object.assign({{ action:'license-validation', module:sent.module||'infant',
                                            valid:true, status:'license-validation-success',
                                            message:'OK' }}, INFANT_READY));
                    inject(INFANT_READY, 300);
                    return;
                }}
                if (act === 'open') {{
                    console.log('[Proxy] DEV intercept open → inject status:initialized + PASS-THROUGH');
                    inject(Object.assign({{ status:'initialized', module:sent.module||'infant' }}, INFANT_READY));
                    inject(INFANT_READY, 400);
                    try {{ _wsSend(data); }} catch(e) {{ console.log('[Proxy] DEV open WS pass-through falhou (WS fechado):', e.message); }}
                    return;
                }}
                // SPA envia action:'start' (não 'start-preview') em startPreview()
                // SPA escuta t.status==="preview-started" (NÃO action:preview-started)
                if (act === 'start' || act === 'start-preview') {{
                    console.log('[Proxy] DEV intercept start → inject status:preview-started + PASS-THROUGH');
                    inject(Object.assign({{ status:'preview-started', module:sent.module||'infant', ret:0 }}, INFANT_READY));
                    // Keep-alive: reinjetar INFANT_READY a cada 5s para manter "device conectado" no SPA
                    if (!_keepAliveInterval) {{
                        _keepAliveInterval = setInterval(function() {{
                            ws.dispatchEvent(new MessageEvent('message', {{data: JSON.stringify(INFANT_READY)}}));
                        }}, 5000);
                    }}
                    try {{ _wsSend(data); }} catch(e) {{ console.log('[Proxy] DEV start WS pass-through falhou (WS fechado):', e.message); }}
                    return;
                }}
                // SPA chama setProcessorFingers() → envia action:'set-processor-fingers'
                // SPA escuta t.status==="done-setting-fingers" → chama stopPreview()+startPreview()
                if (act === 'set-processor-fingers') {{
                    console.log('[Proxy] DEV intercept set-processor-fingers → inject done-setting-fingers + PASS-THROUGH');
                    inject(Object.assign({{ status:'done-setting-fingers', module:sent.module||'infant' }}, INFANT_READY));
                    try {{ _wsSend(data); }} catch(e) {{ console.log('[Proxy] DEV set-processor-fingers WS falhou:', e.message); }}
                    return;
                }}
                if (act === 'stop' || act === 'stop-preview') {{
                    inject(Object.assign({{ action:'stop-response', module:sent.module||'infant',
                                            status:'success' }}, INFANT_READY));
                    if (_keepAliveInterval) {{ clearInterval(_keepAliveInterval); _keepAliveInterval = null; }}
                    try {{ _wsSend(data); }} catch(e) {{}}
                    return;
                }}
                if (act === 'capture') {{
                    // Tentar SOAP REST primeiro → mais confiável que WS quando há problema de licença
                    var _capFinger = sent.fingerIndex !== undefined ? sent.fingerIndex :
                                     (sent.positionIndex !== undefined ? sent.positionIndex : 0);
                    console.log('[Proxy] DEV capture → SOAP REST (fingerIndex=' + _capFinger + ') + WS fallback');
                    fetch(BASE + '/api/etan/capture', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{fingerIndex: _capFinger}})
                    }})
                    .then(function(r) {{ return r.json(); }})
                    .then(function(d) {{
                        if (d.success && d.finger) {{
                            inject(Object.assign({{
                                status: 'captured', module: sent.module || 'infant', ret: 0,
                                data: {{
                                    wsqData: d.finger.wsqData || '',
                                    imagePng: d.finger.wsqData || '',
                                    nfiq: d.finger.nfiqScore || 2,
                                    fingerIndex: _capFinger,
                                    anomalyId: '', anomalyName: ''
                                }}
                            }}, INFANT_READY));
                            console.log('[Proxy] DEV capture SOAP ok → NFIQ=' + (d.finger.nfiqScore || 2));
                        }} else {{
                            // SOAP indisponível (ETAN não conectado) → tentar WS direto
                            console.log('[Proxy] DEV capture SOAP indisponível (' + (d.error || 'sem ETAN') + ') → WS pass-through');
                            try {{ _wsSend(data); }} catch(e) {{ console.log('[Proxy] DEV capture WS pass-through falhou:', e.message); }}
                        }}
                    }})
                    .catch(function(e) {{
                        console.log('[Proxy] DEV capture SOAP erro de rede → WS pass-through:', e.message);
                        try {{ _wsSend(data); }} catch(e2) {{ console.log('[Proxy] DEV capture WS falhou:', e2.message); }}
                    }});
                    return;
                }}
                if (act === 'fetch-module-configs') {{
                    inject({{ action:'module-configs-response',
                               configs:{{ infant:{{ enabled:true, licensed:true, active:true,
                                                    captureTimeout:30000, maxAttempts:5, minQuality:30,
                                                    autoCapture:true, liveCapture:true }},
                                          face:{{ enabled:true }}, signature:{{ enabled:true }},
                                          modal:{{ enabled:true }} }} }});
                    return;
                }}
                if (act === 'fetch-offline-settings') {{
                    inject({{ action:'offline-settings-response',
                               settings:{{ infant:{{ enabled:true }}, liveCapture:true }} }});
                    return;
                }}
            }} catch(e) {{}}

            // Catch-all Device WS: PASSAR para OpenBio (keepalive/heartbeat, match, etc.)
            console.log('[Proxy] DEV WS PASS-THROUGH (unhandled):', data.substring(0,100));
            try {{ return _wsSend(data); }} catch(e) {{ console.log('[Proxy] DEV catch-all WS falhou:', e.message); }}
        }};

        var origAdd = ws.addEventListener.bind(ws);
        if (isDevice) {{
            origAdd('open',  function() {{ _realWsOpened = true; }});
            origAdd('close', function() {{ _isDeviceWsClosed = true; }});
            // Se o WS real não abrir em 2s (conexão recusada/erro), disparar open sintético
            // para que o SPA execute sua inicialização normalmente.
            setTimeout(function() {{
                if (!_realWsOpened) {{
                    console.log('[Proxy] DEV WS não abriu em 2s → disparo de open sintético');
                    ws.dispatchEvent(new Event('open'));
                    inject(INFANT_READY, 100);
                    inject(INFANT_READY, 700);
                }}
            }}, 2000);
        }}
        ws.addEventListener = function(type, handler, opts) {{
            if (type === 'message') {{
                return origAdd(type, function(evt) {{
                    if (evt.data && evt.data.length < 2000)
                        console.log('[Proxy] WS recv:', pUrl.split('/').pop(), evt.data.substring(0,300));
                    var p = patchWsMessage(evt.data);
                    if (p === null) {{ console.log('[Proxy] WS msg BLOQUEADA (null)'); return; }}
                    handler(p !== evt.data ? new MessageEvent('message', {{data:p,origin:evt.origin}}) : evt);
                }}, opts);
            }}
            if (type === 'open') {{
                return origAdd(type, function(evt) {{
                    handler(evt);
                    // Injetar INFANT_READY em AMBOS os canais (device e interface)
                    // SDK 0.0.3.0: interface WS não reporta infant → precisamos injetar
                    var delay1 = isDevice ? 400 : 600;
                    var delay2 = isDevice ? 900 : 1500;
                    inject(INFANT_READY, delay1);
                    inject(INFANT_READY, delay2);
                }}, opts);
            }}
            if (isDevice && (type === 'close' || type === 'error')) {{
                console.log('[Proxy] DEV WS ' + type + ' SUPRIMIDO');
                return;
            }}
            return origAdd(type, handler, opts);
        }};

        var _onopen = null;
        Object.defineProperty(ws, 'onopen', {{
            get: function() {{ return _onopen; }},
            set: function(fn) {{
                _onopen = fn;
                origAdd('open', function(evt) {{
                    if (_onopen) _onopen(evt);
                    var delay1 = isDevice ? 400 : 600;
                    var delay2 = isDevice ? 900 : 1500;
                    inject(INFANT_READY, delay1);
                    inject(INFANT_READY, delay2);
                }});
            }},
            configurable: true
        }});

        var _onmsg = null;
        Object.defineProperty(ws, 'onmessage', {{
            get: function() {{ return _onmsg; }},
            set: function(fn) {{
                _onmsg = fn;
                origAdd('message', function(evt) {{
                    if (!_onmsg) return;
                    if (evt.data && evt.data.length < 2000)
                        console.log('[Proxy] WS recv (onmsg):', pUrl.split('/').pop(), evt.data.substring(0,300));
                    var p = patchWsMessage(evt.data);
                    if (p === null) {{ console.log('[Proxy] WS msg BLOQUEADA (null, onmsg)'); return; }}
                    _onmsg(p !== evt.data ? new MessageEvent('message', {{data:p,origin:evt.origin}}) : evt);
                }});
            }},
            configurable: true
        }});

        if (isDevice) {{
            var _onclose = null, _onerror = null;
            Object.defineProperty(ws, 'onclose', {{
                get: function() {{ return _onclose; }},
                set: function(fn) {{ _onclose = fn; console.log('[Proxy] DEV WS onclose SUPRIMIDO'); }},
                configurable: true
            }});
            Object.defineProperty(ws, 'onerror', {{
                get: function() {{ return _onerror; }},
                set: function(fn) {{ _onerror = fn; console.log('[Proxy] DEV WS onerror SUPRIMIDO'); }},
                configurable: true
            }});
            Object.defineProperty(ws, 'readyState', {{
                get: function() {{ return 1; }},
                configurable: true
            }});
        }}

        return ws;
    }};
    Object.setPrototypeOf(window.WebSocket, _WS);
    window.WebSocket.CONNECTING = _WS.CONNECTING;
    window.WebSocket.OPEN = _WS.OPEN;
    window.WebSocket.CLOSING = _WS.CLOSING;
    window.WebSocket.CLOSED = _WS.CLOSED;

    console.log('[InfantProxy] Interceptor ativo. Customer:', CUSTOMER_ID);
}})();
</script>"""


# Headers que nunca devem chegar ao backend (causa 304 no polling)
_CACHE_HEADERS = {'if-none-match', 'if-modified-since', 'if-match',
                  'if-unmodified-since', 'if-range', 'cache-control', 'pragma'}

def _proxy_headers(headers):
    excluded = EXCLUDED_REQ_HEADERS | _CACHE_HEADERS
    return {k: v for k, v in headers.items()
            if k.lower() not in excluded}


# ─────────────────────────────────────────────────────────────
# Detecção automática de versão do SDK ETAN/OpenBio
# Agnóstico de versão: suporta qualquer SDK presente sem alterar código
# ─────────────────────────────────────────────────────────────
_SDK_CACHE: dict = {'version': '0.3.0.0', 'ts': 0.0}  # fallback razoável
_SDK_TTL = 30  # segundos — redetectar a cada 30s


def _detect_infant_sdk_version() -> str:
    """Detecta automaticamente a versão do SDK infant do OpenBio em execução.

    Estratégias (em ordem): REST /db/api/settings → REST /db/api/status →
    REST /db/api/devices/status → SOAP getVersion → última versão conhecida.
    Cache de 30 segundos: transparente quando OpenBio reinicia com SDK diferente.
    """
    import time
    now = time.time()
    if now - _SDK_CACHE['ts'] < _SDK_TTL:
        return _SDK_CACHE['version']

    ver = _sdk_from_openbio_rest() or _sdk_from_soap_version() or _SDK_CACHE['version']
    _SDK_CACHE.update({'version': ver, 'ts': now})
    return ver


def _sdk_from_openbio_rest() -> 'str | None':
    """Detecta versão SDK via REST API do OpenBio (localhost:5000)."""
    for endpoint in ('/db/api/settings', '/db/api/status', '/db/api/devices/status'):
        try:
            r = req_lib.get(f'http://localhost:5000{endpoint}',
                            timeout=1.5, headers={'Cache-Control': 'no-cache'})
            if r.status_code == 200:
                d = r.json()
                ver = (d.get('infant', {}).get('sdkVersion') or
                       d.get('infantSdkVersion') or
                       d.get('sdkVersion') or
                       d.get('version'))
                if ver and isinstance(ver, str) and ver.count('.') >= 2:
                    return ver
        except Exception:
            pass
    return None


def _sdk_from_soap_version() -> 'str | None':
    """Detecta versão SDK via SOAP do ETAN (localhost:12339)."""
    try:
        if not _etan_soap_available():
            return None
        xml = _soap_call('<tns:getVersion><optionalMessage></optionalMessage></tns:getVersion>',
                         timeout=2)
        if xml:
            import re as _re
            m = _re.search(
                r'<(?:version|sdkVersion|infantVersion|infantSdkVersion)>([^<]+)</[^>]+>',
                xml, _re.I)
            if m:
                ver = m.group(1).strip()
                if ver and ver.count('.') >= 2:
                    return ver
    except Exception:
        pass
    return None


def _build_response(resp):
    content_type = resp.headers.get('Content-Type', '')

    if 'text/html' in content_type:
        sdk_ver = _detect_infant_sdk_version()
        script = INTERCEPTOR_SCRIPT.replace('__ETAN_SDK__', sdk_ver)
        html = resp.content.decode('utf-8', errors='replace')
        if '<head>' in html.lower():
            idx = html.lower().index('<head>') + len('<head>')
            html = html[:idx] + script + html[idx:]
        else:
            html = script + html
        content = html.encode('utf-8')
    else:
        content = resp.content

    headers = {k: v for k, v in resp.headers.items()
               if k.lower() not in EXCLUDED_RES_HEADERS}
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Private-Network'] = 'true'

    return Response(content, status=resp.status_code, headers=headers)


# ─────────────────────────────────────────────────────────────
# PROXY: infant.akiyama.com.br  (não seguir redirect para plataformaid)
# ─────────────────────────────────────────────────────────────

@bp.route('/infant/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD'])
@bp.route('/infant/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD'])
def infant_proxy(path):
    target = f"{INFANT_ORIGIN}/{path}"
    if request.query_string:
        target += '?' + request.query_string.decode('utf-8')

    try:
        resp = req_lib.request(
            method=request.method,
            url=target,
            headers=_proxy_headers(dict(request.headers)),
            data=request.get_data(),
            allow_redirects=False,   # ← não seguir redirect para plataformaid
            timeout=15,
            verify=False
        )
        # Se redirecionou para plataformaid (login), servir a raiz do infant direto
        location = resp.headers.get('Location', '')
        if resp.status_code in (301, 302, 303, 307, 308) and 'plataformaid' in location:
            resp = req_lib.get(INFANT_ORIGIN + '/', allow_redirects=False,
                               timeout=15, verify=False)
        return _build_response(resp)
    except req_lib.exceptions.ConnectionError:
        return Response("Infant proxy: sem conexão com o servidor remoto.", status=502)
    except req_lib.exceptions.Timeout:
        return Response("Infant proxy: timeout.", status=504)


# ─────────────────────────────────────────────────────────────
# PROXY: localhost:5000 (OpenBio)
# ─────────────────────────────────────────────────────────────

@bp.route('/openbio/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD'])
@bp.route('/openbio/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD'])
def openbio_proxy(path):
    target = f"{OPENBIO_ORIGIN}/{path}"
    if request.query_string:
        target += '?' + request.query_string.decode('utf-8')

    try:
        # Forçar requisição fresca — nunca repassar headers de cache ao openbio
        fresh_headers = _proxy_headers(dict(request.headers))
        fresh_headers['Cache-Control'] = 'no-cache, no-store'
        fresh_headers['Pragma'] = 'no-cache'
        resp = req_lib.request(
            method=request.method,
            url=target,
            headers=fresh_headers,
            data=request.get_data(),
            allow_redirects=True,
            timeout=10
        )
        body = resp.content
        # Injetar customerId e ativar licença infant no retorno do config e settings
        if ('config' in path or 'settings' in path) and 'application/json' in resp.headers.get('Content-Type', ''):
            try:
                data = json.loads(body)
                if not data.get('customerId'):
                    data['customerId'] = CUSTOMER_UUID
                if 'enrollmentValidations' in data:
                    data['enrollmentValidations']['infant'] = True
                data['showInfantTab'] = True

                # ── Capturar versão real do SDK da resposta do OpenBio → atualiza cache imediatamente
                import time as _time
                _actual_sdk = (data.get('infant', {}).get('sdkVersion') or
                               data.get('infantSdkVersion') or data.get('sdkVersion'))
                if _actual_sdk and isinstance(_actual_sdk, str) and _actual_sdk.count('.') >= 2:
                    _SDK_CACHE.update({'version': _actual_sdk, 'ts': _time.time()})

                # Dispositivo ETAN para finger e infant
                ETAN_DEVICE = {
                    'id': 'EtanV2',
                    'name': 'ETAN V2',
                    'type': 'infant',
                    'vendor': 'ETAN',
                    'model': 'EtanV2',
                    'status': 'connected',
                    'initialized': True,
                    'enabled': True,
                    'loaded': True,
                    'ready': True,
                    'loading': False,
                }
                if 'infant' in data:
                    data['infant']['device'] = ETAN_DEVICE   # sempre forçar
                    data['infant']['enabled'] = True
                if 'finger' in data:
                    data['finger']['device'] = ETAN_DEVICE   # sempre forçar
                    data['finger']['canUseInfant'] = True    # ← CRÍTICO: habilita módulo infant
                # Garantir auto-start do dispositivo ao carregar a SPA
                data['startDevicesOnRun'] = True
                body = json.dumps(data).encode('utf-8')
            except Exception:
                pass
        headers = {k: v for k, v in resp.headers.items()
                   if k.lower() not in EXCLUDED_RES_HEADERS}
        headers['Access-Control-Allow-Origin'] = '*'
        headers['Access-Control-Allow-Private-Network'] = 'true'
        return Response(body, status=resp.status_code, headers=headers)
    except req_lib.exceptions.ConnectionError:
        return Response('{"error":"OpenBio offline"}', status=503,
                        headers={'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'})
    except req_lib.exceptions.Timeout:
        return Response('{"error":"OpenBio timeout"}', status=504,
                        headers={'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'})


# ─────────────────────────────────────────────────────────────
# PROXY: APIs externas Akiyama  → mock quando 401/403
# /akiyama-api/management/<path> → api-management.akiyama.com.br
# /akiyama-api/enroll/<path>     → api-enroll.akiyama.com.br
# ─────────────────────────────────────────────────────────────

AKIYAMA_HOSTS = {
    'management': 'https://api-management.akiyama.com.br',
    'enroll':     'https://api-enroll.akiyama.com.br',
}

@bp.route('/akiyama-api/<api>/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD'])
@bp.route('/akiyama-api/<api>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD'])
def akiyama_proxy(api, path):
    host = AKIYAMA_HOSTS.get(api)
    if not host:
        return _mock_json({'error': f'API desconhecida: {api}'}, 404)

    target = f"{host}/{path}"
    if request.query_string:
        target += '?' + request.query_string.decode('utf-8')

    if request.method == 'OPTIONS':
        return Response('', status=200, headers={'Access-Control-Allow-Origin': '*',
                                                  'Access-Control-Allow-Headers': '*',
                                                  'Access-Control-Allow-Methods': '*'})

    # ── Retornar mock DIRETAMENTE para endpoints conhecidos (sem bater no servidor externo)
    # Corrigir customer/undefined → usar CUSTOMER_UUID
    if 'undefined' in path:
        path = path.replace('undefined', CUSTOMER_UUID)
        target = f"{host}/{path}"
        if request.query_string:
            target += '?' + request.query_string.decode('utf-8')

    combined = (path + '?' + request.query_string.decode('utf-8', errors='replace')).lower()
    # Endpoints de localização/tradução (SDK 0.3.0.0+) → RegisterClientLocalizationsError sem este mock
    if any(x in combined for x in ['localiz', 'translat', 'i18n', 'locale', 'language']):
        return _mock_json({
            'translations': {}, 'locale': 'pt-BR', 'language': 'pt-BR',
            'status': 'ok', 'customerId': CUSTOMER_UUID,
            'data': {'translations': {}, 'locale': 'pt-BR'},
        })
    if 'account-logged-user' in combined or 'account-logged' in combined:
        return _mock_json(MOCK_ACCOUNT_USER)
    if 'form_type' in combined or 'formtype' in combined:
        return _mock_json(MOCK_FORM_TYPE)
    if 'dynamic-forms-customer' in combined or 'dynamicform' in combined:
        return _mock_json(MOCK_DYNAMIC_FORMS)
    # customer/{id}/config ou customer/{id}/settings
    if 'customer/' in combined and ('/config' in combined or '/setting' in combined or '/con' in combined):
        return _mock_json({
            'customerId': CUSTOMER_UUID,
            'id': CUSTOMER_UUID,
            'status': 'ACTIVE',
            'infantEnabled': True,
            'modules': {'infant': True, 'fingerprint': True, 'face': True},
            'customerTheme': MOCK_ACCOUNT_USER['customerTheme'],
        })
    # Endpoints de licença / módulos
    if any(x in combined for x in ['license', 'licen', 'module', 'modulo', 'subscription', 'plan', 'feature']):
        return _mock_json({
            'customerId': CUSTOMER_UUID,
            'status': 'ACTIVE',
            'modules': [
                {'name': 'infant', 'status': 'ACTIVE', 'enabled': True, 'licensed': True},
                {'name': 'fingerprint', 'status': 'ACTIVE', 'enabled': True, 'licensed': True},
                {'name': 'face', 'status': 'ACTIVE', 'enabled': True, 'licensed': True},
            ],
            'licenses': [
                {'module': 'infant', 'status': 'ACTIVE', 'valid': True, 'customerId': CUSTOMER_UUID},
                {'module': 'fingerprint', 'status': 'ACTIVE', 'valid': True, 'customerId': CUSTOMER_UUID},
            ],
            'infantLicense': {'status': 'ACTIVE', 'valid': True, 'customerId': CUSTOMER_UUID},
            'hasInfantLicense': True,
            'hasInfantModule': True,
            'infantEnabled': True,
        })

    try:
        resp = req_lib.request(
            method=request.method,
            url=target,
            headers=_proxy_headers(dict(request.headers)),
            data=request.get_data(),
            allow_redirects=True,
            timeout=10,
            verify=False
        )

        if resp.status_code in (401, 403):
            # Retornar mock com campos essenciais para evitar crash da SPA
            return _mock_json({
                'status': 'ok', 'customerId': CUSTOMER_UUID,
                'translations': {}, 'locale': 'pt-BR',
                'data': None, 'content': [],
            })

        headers = {k: v for k, v in resp.headers.items()
                   if k.lower() not in EXCLUDED_RES_HEADERS}
        headers['Access-Control-Allow-Origin'] = '*'
        return Response(resp.content, status=resp.status_code, headers=headers)

    except (req_lib.exceptions.ConnectionError, req_lib.exceptions.Timeout):
        return _mock_json({
            'status': 'ok', 'customerId': CUSTOMER_UUID,
            'translations': {}, 'locale': 'pt-BR',
            'data': None, 'content': [],
        })


# ─────────────────────────────────────────────────────────────
# ETAN SOAP Client  (http://127.0.0.1:12339/)
# + session.json manager (AppData\Roaming\OpenbioDevices\session.json)
# ─────────────────────────────────────────────────────────────

SESSION_JSON_PATH = os.path.join(
    os.environ.get('APPDATA', r'C:\Users\Default\AppData\Roaming'),
    'OpenbioDevices', 'session.json'
)
ETAN_SOAP_URL  = 'http://127.0.0.1:12339/'
ETAN_SOAP_HTTPS = 'https://127.0.0.1:12339/'

POSITION_TO_INDEX = {
    'RIGHT-THUMB': 0, 'RIGHT-INDEX': 1, 'RIGHT-MIDDLE': 2,
    'RIGHT-RING': 3, 'RIGHT-LITTLE': 4,
    'LEFT-THUMB': 5, 'LEFT-INDEX': 6, 'LEFT-MIDDLE': 7,
    'LEFT-RING': 8, 'LEFT-LITTLE': 9
}
INDEX_TO_POSITION = {v: k for k, v in POSITION_TO_INDEX.items()}


def _etan_soap_available():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex(('127.0.0.1', 12339))
        s.close()
        return result == 0
    except Exception:
        return False


def _soap_call(body_xml, timeout=30):
    envelope = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="tns">'
        '<env:Body>' + body_xml + '</env:Body></env:Envelope>'
    )
    hdrs = {'Content-Type': 'text/xml; charset=utf-8', 'SOAPAction': ''}
    for url in [ETAN_SOAP_URL, ETAN_SOAP_HTTPS]:
        try:
            r = req_lib.post(url, data=envelope.encode('utf-8'), headers=hdrs,
                             timeout=timeout, verify=False)
            if r.status_code == 200:
                return r.text
        except Exception:
            continue
    return None


def _soap_init_capture(flow_type=0):
    return _soap_call(
        '<tns:initCapture>'
        '<optionalMessage></optionalMessage>'
        '<singleCapture>true</singleCapture>'
        '<cpf></cpf>'
        '<useOpenbioMatcher>false</useOpenbioMatcher>'
        f'<flowType>{flow_type}</flowType>'
        '</tns:initCapture>'
    )


def _soap_capture_finger(position='RIGHT-THUMB'):
    return _soap_call(
        f'<tns:captureOneFinger>'
        f'<position>{position}</position>'
        f'<captureType>0</captureType>'
        f'</tns:captureOneFinger>',
        timeout=30
    )


def _soap_get_fingers():
    return _soap_call(
        '<tns:getFingers><optionalMessage></optionalMessage></tns:getFingers>',
        timeout=5
    )


def _parse_soap_fingers(xml_text):
    try:
        root = ET.fromstring(xml_text)
        fingers = []
        for output in root.iter('output'):
            f = {}
            for child in output:
                tag = child.tag.split('}')[-1]
                f[tag] = child.text or ''
            fingers.append(f)
        return fingers
    except Exception:
        return []


def _read_session():
    try:
        with open(SESSION_JSON_PATH, 'r', encoding='utf-8') as fh:
            return json.load(fh)
    except Exception:
        return {'session': {
            'createdAt': '', 'updatedAt': '', 'sequence': [], 'status': 1,
            'data': [], 'infantData': [], 'signature': {}, 'photo': {},
            'mugshot': {'index': 0, 'description': ''}, 'mugshots': [],
            'palm': {'device': {}, 'captures': []}, 'auth': {'result': 'aborted'},
            'captureType': 0, 'position': '', 'cpf': ''
        }}


def _write_session(data):
    with open(SESSION_JSON_PATH, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)


def _upsert_infant_finger(finger_record):
    data = _read_session()
    idx = finger_record.get('fingerIndex', 0)
    data['session']['infantData'] = [
        f for f in data['session']['infantData'] if f.get('fingerIndex') != idx
    ]
    data['session']['infantData'].append(finger_record)
    _write_session(data)
    return data['session']['infantData']


def _cors_ok(methods='GET, POST, DELETE, OPTIONS'):
    return {'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': methods,
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'application/json'}


# ─── /api/etan/status ────────────────────────────────────────
@bp.route('/api/etan/status', methods=['GET', 'OPTIONS'])
def api_etan_status():
    if request.method == 'OPTIONS':
        return Response('', status=204, headers=_cors_ok())
    available = _etan_soap_available()
    return Response(
        json.dumps({'available': available, 'port': 12339,
                    'sessionPath': SESSION_JSON_PATH}),
        status=200, headers=_cors_ok()
    )


# ─── /api/etan/capture  POST {fingerIndex} ───────────────────
@bp.route('/api/etan/capture', methods=['POST', 'OPTIONS'])
def api_etan_capture():
    if request.method == 'OPTIONS':
        return Response('', status=204, headers=_cors_ok('POST, OPTIONS'))

    body = request.get_json(force=True) or {}
    finger_index = int(body.get('fingerIndex', 0))
    position = INDEX_TO_POSITION.get(finger_index, 'RIGHT-THUMB')

    if not _etan_soap_available():
        return Response(
            json.dumps({'error': 'ETAN SOAP service não disponível (porta 12339 fechada). '
                                 'Verifique se o dispositivo ETAN está conectado e o '
                                 'openbio-devices está em execução.'}),
            status=503, headers=_cors_ok()
        )

    # Init capture mode
    _soap_init_capture()

    # Trigger finger capture (blocks until finger placed or timeout)
    result_xml = _soap_capture_finger(position)
    if result_xml is None:
        return Response(json.dumps({'error': 'Timeout ou falha na captura SOAP'}),
                        status=504, headers=_cors_ok())

    # Get captured fingers
    fingers_xml = _soap_get_fingers()
    if not fingers_xml:
        return Response(json.dumps({'error': 'getFingers falhou após captura'}),
                        status=500, headers=_cors_ok())

    parsed = _parse_soap_fingers(fingers_xml)
    if not parsed:
        return Response(json.dumps({'error': 'Nenhum dedo retornado pelo SOAP'}),
                        status=404, headers=_cors_ok())

    soap_finger = parsed[0]
    image_data = soap_finger.get('imagePng', soap_finger.get('imageFlat', ''))

    finger_record = {
        'fingerIndex': finger_index,
        'nfiqScore': 2,
        'wsqData': image_data,
        'segmentedData': image_data,
        'template': '',
        'captureType': 0,
        'anomalyId': '',
        'anomalyName': ''
    }
    all_fingers = _upsert_infant_finger(finger_record)
    return Response(
        json.dumps({'success': True, 'finger': finger_record, 'total': len(all_fingers)}),
        status=200, headers=_cors_ok()
    )


# ─── /api/etan/session  GET/DELETE ───────────────────────────
@bp.route('/api/etan/session', methods=['GET', 'DELETE', 'OPTIONS'])
def api_etan_session():
    if request.method == 'OPTIONS':
        return Response('', status=204, headers=_cors_ok())
    if request.method == 'DELETE':
        data = _read_session()
        data['session']['infantData'] = []
        _write_session(data)
        return Response(json.dumps({'success': True}), status=200, headers=_cors_ok())
    data = _read_session()
    return Response(
        json.dumps({'infantFingers': data.get('session', {}).get('infantData', [])}),
        status=200, headers=_cors_ok()
    )


# ─── /api/etan/save-finger  POST {finger object} ─────────────
@bp.route('/api/etan/save-finger', methods=['POST', 'OPTIONS'])
def api_etan_save_finger():
    """Accepts finger data from SPA (fetch interceptor redirect) and saves to session.json"""
    if request.method == 'OPTIONS':
        return Response('', status=204, headers=_cors_ok('POST, OPTIONS'))
    finger_data = request.get_json(force=True) or {}
    if not finger_data:
        return Response(json.dumps({'error': 'No data'}), status=400, headers=_cors_ok())
    all_fingers = _upsert_infant_finger(finger_data)
    return Response(
        json.dumps({'success': True, 'total': len(all_fingers)}),
        status=200, headers=_cors_ok()
    )


# ─── Intercept DELETE on /openbio/db/api/detached-biometries/infant ──
# openbio-devices returns 404 for DELETE; we handle it ourselves.
@bp.route('/openbio/db/api/detached-biometries/infant', methods=['DELETE', 'OPTIONS'])
def openbio_clear_infant_session():
    if request.method == 'OPTIONS':
        return Response('', status=204, headers=_cors_ok())
    data = _read_session()
    data['session']['infantData'] = []
    _write_session(data)
    return Response(json.dumps({'success': True}), status=200, headers=_cors_ok())
