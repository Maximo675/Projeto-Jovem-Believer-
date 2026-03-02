/**
 * 🖐️ OPENBIO BRIDGE - Integração com SDK Openbio Real
 * Conecta frontend com hardware biométrico de verdade
 * 
 * Porta: 3333
 * Url base: http://localhost:3333/api
 */

const express = require('express');
const cors = require('cors');
const http = require('http');
const fetch = require('node-fetch');

const app = express();
const server = http.createServer(app);
const PORT = 3333;

// ============================================================
// MIDDLEWARE
// ============================================================
app.use(cors());
app.use(express.json());

// ============================================================
// CONFIGURAÇÃO OPENBIO
// ============================================================
const OPENBIO_CONFIGS = {
  apiService: 'http://localhost:4000',
  localService: 'http://localhost:4001'
};

console.log(`
╔════════════════════════════════════════════════════════════╗
║         🖐️  OPENBIO BRIDGE SERVER INICIANDO              ║
║                                                            ║
║  Device Service:  ${OPENBIO_CONFIGS.deviceService}                    ║
║  API Service:     ${OPENBIO_CONFIGS.apiService}                      ║
║  Local Service:   ${OPENBIO_CONFIGS.localService}                    ║
║                                                            ║
║  Proxy Server:    http://localhost:${PORT}                         ║
╚════════════════════════════════════════════════════════════╝
`);

// ============================================================
// HEALTH CHECK - Verificar conexão com Openbio
// ============================================================
app.get('/health', async (req, res) => {
  try {
    // Tentar conectar com Openbio Device Service
    const response = await fetch(`${OPENBIO_CONFIGS.deviceService}/health`, {
      timeout: 5000
    }).catch(e => ({ ok: false, error: e.message }));

    if (response.ok) {
      return res.json({
        status: 'ok',
        openbio: 'connected',
        services: {
          deviceService: '✅ online',
          apiService: '✅ online',
          localService: '✅ online'
        }
      });
    } else {
      return res.status(503).json({
        status: 'offline',
        openbio: 'disconnected',
        message: 'Openbio services não responderam',
        error: response.error
      });
    }
  } catch (error) {
    res.status(503).json({
      status: 'offline',
      openbio: 'error',
      message: error.message
    });
  }
});

// ============================================================
// 🖐️ CAPTURA BIOMÉTRICA - Impressão Digital
// ============================================================
app.post('/api/fingerprint/capture', async (req, res) => {
  try {
    const { deviceId = 'default', finger = 'thumb_left', timeoutMs = 5000 } = req.body;

    console.log(`\n📸 Iniciando captura de digital...`);
    console.log(`   Dispositivo: ${deviceId}`);
    console.log(`   Dedo: ${finger}`);

    // Tentar capturar pelo Openbio Device Service (hardware real)
    const captureResponse = await fetch(
      `${OPENBIO_CONFIGS.deviceService}/api/biometrics/fingerprint/capture`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          deviceId,
          finger,
          mode: 'infant', // Modo para recém-nascidos
          timeout: timeoutMs
        })
      }
    );

    if (!captureResponse.ok) {
      throw new Error(`Openbio retornou: ${captureResponse.status}`);
    }

    const captureData = await captureResponse.json();

    console.log(`✅ Captura bem-sucedida!`);
    console.log(`   NFIQ Score: ${captureData.nfiq || 'N/A'}`);
    console.log(`   Qualidade: ${captureData.quality || 'N/A'}%`);

    return res.json({
      success: true,
      source: 'openbio_real',
      data: captureData,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error(`❌ Erro na captura:`, error.message);
    
    // FALLBACK: Retornar erro sem tentar simulação
    res.status(503).json({
      success: false,
      source: 'openbio',
      error: error.message,
      suggestion: 'Verifique se Openbio Device Service está rodando (porta 5000)'
    });
  }
});

// ============================================================
// 🎥 PREVIEW DE CAPTURA - Feedback ao vivo
// ============================================================
app.post('/api/fingerprint/preview', async (req, res) => {
  try {
    const { deviceId = 'default', finger = 'thumb_left' } = req.body;

    // Solicitar preview ao Openbio
    const previewResponse = await fetch(
      `${OPENBIO_CONFIGS.deviceService}/api/biometrics/fingerprint/preview`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ deviceId, finger })
      }
    );

    if (!previewResponse.ok) {
      throw new Error('Não foi possível obter preview');
    }

    const previewData = await previewResponse.json();

    return res.json({
      success: true,
      data: previewData,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    res.status(503).json({
      success: false,
      error: error.message
    });
  }
});

// ============================================================
// 📸 LISTAR DISPOSITIVOS DISPONÍVEIS
// ============================================================
app.get('/api/devices', async (req, res) => {
  try {
    const devicesResponse = await fetch(
      `${OPENBIO_CONFIGS.deviceService}/api/devices`,
      { timeout: 5000 }
    );

    if (!devicesResponse.ok) {
      throw new Error('Não foi possível lister dispositivos');
    }

    const devices = await devicesResponse.json();

    return res.json({
      success: true,
      devices: devices,
      count: devices.length
    });

  } catch (error) {
    res.status(503).json({
      success: false,
      error: error.message,
      message: 'Openbio Device Service não está respondendo'
    });
  }
});

// ============================================================
// ✅ VERIFICAR STATUS DO DISPOSITIVO
// ============================================================
app.get('/api/devices/:deviceId/status', async (req, res) => {
  try {
    const { deviceId } = req.params;

    const statusResponse = await fetch(
      `${OPENBIO_CONFIGS.deviceService}/api/devices/${deviceId}/status`,
      { timeout: 5000 }
    );

    if (!statusResponse.ok) {
      throw new Error('Dispositivo não encontrado');
    }

    const status = await statusResponse.json();

    return res.json({
      success: true,
      deviceId,
      status: status
    });

  } catch (error) {
    res.status(503).json({
      success: false,
      error: error.message
    });
  }
});

// ============================================================
// ROTAS DE TESTE
// ============================================================
app.get('/test/devices', async (req, res) => {
  try {
    console.log('\n🧪 Testando conexão com Openbio...\n');

    // Test 1: Device Service
    console.log('1️⃣  Testando Device Service (5000)...');
    try {
      const deviceTest = await fetch(`${OPENBIO_CONFIGS.deviceService}/health`, { timeout: 3000 });
      console.log(deviceTest.ok ? '✅ Device Service OK' : '❌ Device Service respondeu com erro');
    } catch (e) {
      console.log('❌ Device Service NÃO está rodando');
    }

    // Test 2: API Service
    console.log('2️⃣  Testando API Service (4000)...');
    try {
      const apiTest = await fetch(`${OPENBIO_CONFIGS.apiService}/health`, { timeout: 3000 });
      console.log(apiTest.ok ? '✅ API Service OK' : '❌ API Service respondeu com erro');
    } catch (e) {
      console.log('❌ API Service NÃO está rodando');
    }

    // Test 3: Local Service
    console.log('3️⃣  Testando Local Service (4001)...');
    try {
      const localTest = await fetch(`${OPENBIO_CONFIGS.localService}/health`, { timeout: 3000 });
      console.log(localTest.ok ? '✅ Local Service OK' : '❌ Local Service respondeu com erro');
    } catch (e) {
      console.log('❌ Local Service NÃO está rodando');
    }

    console.log('\n');
    res.json({ message: 'Teste completado. Verifique o console.' });

  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ============================================================
// INICIAR SERVIDOR
// ============================================================
server.listen(PORT, () => {
  console.log(`\n🚀 Servidor rodando em http://localhost:${PORT}\n`);
  console.log('📋 Endpoints disponíveis:');
  console.log('   GET  /health                    - Status do servidor');
  console.log('   POST /api/fingerprint/capture   - Capturar digital');
  console.log('   POST /api/fingerprint/preview   - Preview ao vivo');
  console.log('   GET  /api/devices               - Listar dispositivos');
  console.log('   GET  /api/devices/:id/status    - Status do dispositivo');
  console.log('   GET  /test/devices              - Testar conexão com Openbio');
  console.log('\n');
});

process.on('uncaughtException', (error) => {
  console.error('❌ Erro não tratado:', error);
});
