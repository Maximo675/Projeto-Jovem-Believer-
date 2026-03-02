/**
 * ETAN Simulator Manager
 * Gerencia o fluxo completo de captura biométrica com múltiplos dedos
 * Integra qualidade de digital, sequência de dedos e documentação
 */

class ETANSimulatorManager {
    constructor(options = {}) {
        this.userId = options.userId || 1;
        this.activityId = options.activityId || 4;
        this.courseId = options.courseId || 1;
        
        // Sequência de dedos ETAN: Polegar, Índice, Meio, Anular, Mínimo (mão direita + esquerda)
        this.fingerSequence = [
            { id: 1, name: 'Polegar', hand: 'Direita', order: 1 },
            { id: 2, name: 'Índice', hand: 'Direita', order: 2 },
            { id: 3, name: 'Meio', hand: 'Direita', order: 3 },
            { id: 4, name: 'Anular', hand: 'Direita', order: 4 },
            { id: 5, name: 'Mínimo', hand: 'Direita', order: 5 },
            { id: 6, name: 'Polegar', hand: 'Esquerda', order: 6 },
            { id: 7, name: 'Índice', hand: 'Esquerda', order: 7 },
            { id: 8, name: 'Meio', hand: 'Esquerda', order: 8 },
            { id: 9, name: 'Anular', hand: 'Esquerda', order: 9 },
            { id: 10, name: 'Mínimo', hand: 'Esquerda', order: 10 }
        ];
        
        this.currentFingerIndex = 0;
        this.capturedFingers = [];
        this.captureAttempts = [];
        this.activityStartTime = Date.now();
        
        // Configurações de qualidade
        this.qualityThreshold = 60; // Mínimo de qualidade aceitável
        this.maxAttemptsPerFinger = 3; // Máximo de tentativas por dedo
        
        console.log('[ETAN] Gerenciador inicializado');
    }
    
    /**
     * Obtém o dedo atual sendo capturado
     */
    getCurrentFinger() {
        return this.fingerSequence[this.currentFingerIndex];
    }
    
    /**
     * Inicia a captura de um dedo específico
     */
    startFingerCapture(fingerIndex = null) {
        if (fingerIndex !== null) {
            this.currentFingerIndex = fingerIndex;
        }
        
        const finger = this.getCurrentFinger();
        if (!finger) {
            console.log('[ETAN] Todas as digitais foram capturadas!');
            return this.completeCaptureSession();
        }
        
        console.log(`[ETAN] Iniciando captura: ${finger.hand} - ${finger.name} (${finger.order}/10)`);
        
        return {
            fingerIndex: this.currentFingerIndex,
            finger: finger,
            progress: `${finger.order}/10`,
            nextFinger: this.getNextFinger()
        };
    }
    
    /**
     * Obtém o próximo dedo
     */
    getNextFinger() {
        const nextIndex = this.currentFingerIndex + 1;
        if (nextIndex < this.fingerSequence.length) {
            return this.fingerSequence[nextIndex];
        }
        return null;
    }
    
    /**
     * Registra uma captura bem-sucedida
     */
    async recordSuccessfulCapture(quality, metrics = {}) {
        const finger = this.getCurrentFinger();
        
        if (!finger) {
            console.error('[ETAN] Erro: dedo inválido');
            return false;
        }
        
        // Validar qualidade
        if (quality < this.qualityThreshold) {
            console.warn(`[ETAN] Qualidade insuficiente: ${quality}% (mínimo: ${this.qualityThreshold}%)`);
            return false;
        }
        
        const nfiqScore = this.calculateNFIQ(quality);
        const captureData = {
            finger_id: finger.id,
            finger_name: finger.name,
            hand: finger.hand,
            order: finger.order,
            quality: quality,
            nfiq_score: nfiqScore,
            metrics: metrics,
            timestamp: new Date().toISOString(),
            attempt_number: this.getAttemptCount(finger.id) + 1
        };
        
        // Salvar localmente
        this.capturedFingers.push(captureData);
        
        // Enviar para servidor
        try {
            const response = await fetch('/api/activities/biometric/capture', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`
                },
                body: JSON.stringify({
                    user_id: this.userId,
                    activity_id: this.activityId,
                    finger_id: finger.id,
                    finger_name: finger.name,
                    hand: finger.hand,
                    quality: quality,
                    nfiq: nfiqScore,
                    attempt_number: this.getAttemptCount(finger.id) + 1,
                    metrics: metrics,
                    timestamp: captureData.timestamp
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            console.log('[ETAN] ✅ Captura salva no servidor:', data);
            
            // Registrar tentativa
            this.captureAttempts.push({
                finger_id: finger.id,
                attempt_number: captureData.attempt_number,
                success: true,
                quality: quality,
                timestamp: captureData.timestamp
            });
            
            return true;
        } catch (error) {
            console.error('[ETAN] Erro ao salvar captura:', error);
            // Salvar localmente mesmo se falhar no servidor
            return true;
        }
    }
    
    /**
     * Avança para o próximo dedo
     */
    advanceToNextFinger() {
        const currentFinger = this.getCurrentFinger();
        
        if (!currentFinger) {
            console.log('[ETAN] Já capturou todos os dedos');
            return null;
        }
        
        this.currentFingerIndex++;
        
        if (this.currentFingerIndex >= this.fingerSequence.length) {
            console.log('[ETAN] Captura completa! Processando resultados...');
            return this.completeCaptureSession();
        }
        
        return this.startFingerCapture();
    }
    
    /**
     * Volta para o dedo anterior (para retentativa)
     */
    retryCurrentFinger() {
        const finger = this.getCurrentFinger();
        const attemptCount = this.getAttemptCount(finger.id);
        
        if (attemptCount >= this.maxAttemptsPerFinger) {
            console.warn(`[ETAN] Máximo de tentativas atingido para ${finger.name}`);
            return {
                success: false,
                message: 'Máximo de tentativas atingido. Avançando para próximo dedo.',
                nextFinger: this.advanceToNextFinger()
            };
        }
        
        console.log(`[ETAN] Retentando ${finger.name} (tentativa ${attemptCount + 1}/${this.maxAttemptsPerFinger})`);
        return {
            success: true,
            message: `Tentativa ${attemptCount + 1} de ${this.maxAttemptsPerFinger}`,
            finger: this.startFingerCapture()
        };
    }
    
    /**
     * Conta tentativas para um dedo específico
     */
    getAttemptCount(fingerId) {
        return this.captureAttempts.filter(a => a.finger_id === fingerId).length;
    }
    
    /**
     * Calcula NFIQ (National Fingerprint Image Quality)
     */
    calculateNFIQ(quality) {
        if (quality >= 90) return 5;
        if (quality >= 80) return 4;
        if (quality >= 70) return 3;
        if (quality >= 50) return 2;
        return 1;
    }
    
    /**
     * Conclui a sessão de captura
     */
    completeCaptureSession() {
        const totalTime = (Date.now() - this.activityStartTime) / 1000;
        const averageQuality = this.getAverageQuality();
        const successRate = this.getSuccessRate();
        
        const results = {
            session_id: `ETAN_${this.userId}_${Date.now()}`,
            user_id: this.userId,
            activity_id: this.activityId,
            total_fingers_captured: this.capturedFingers.length,
            total_fingers_required: this.fingerSequence.length,
            total_attempts: this.captureAttempts.length,
            average_quality: averageQuality,
            success_rate: successRate,
            total_time: totalTime,
            captured_fingers: this.capturedFingers,
            completion_status: this.capturedFingers.length === this.fingerSequence.length ? 'completed' : 'partial',
            timestamp: new Date().toISOString()
        };
        
        console.log('[ETAN] Sessão concluída:', results);
        
        // Enviar relatório final
        this.sendFinalReport(results);
        
        return results;
    }
    
    /**
     * Envia relatório final ao servidor
     */
    async sendFinalReport(results) {
        try {
            const response = await fetch('/api/activities/biometric/completion', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`
                },
                body: JSON.stringify({
                    user_id: this.userId,
                    activity_id: this.activityId,
                    course_id: this.courseId,
                    total_fingers_captured: results.total_fingers_captured,
                    average_quality: results.average_quality,
                    success_rate: results.success_rate,
                    total_time: results.total_time,
                    captured_fingers: results.captured_fingers,
                    completion_date: new Date().toISOString()
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                console.log('[ETAN] Relatório enviado com sucesso:', data);
            } else {
                console.error('[ETAN] Erro ao enviar relatório:', response.status);
            }
        } catch (error) {
            console.error('[ETAN] Erro ao enviar relatório:', error);
        }
    }
    
    /**
     * Calcula qualidade média
     */
    getAverageQuality() {
        if (this.capturedFingers.length === 0) return 0;
        const sum = this.capturedFingers.reduce((acc, f) => acc + f.quality, 0);
        return Math.round(sum / this.capturedFingers.length);
    }
    
    /**
     * Calcula taxa de sucesso
     */
    getSuccessRate() {
        if (this.captureAttempts.length === 0) return 0;
        const successCount = this.captureAttempts.filter(a => a.success).length;
        return Math.round((successCount / this.captureAttempts.length) * 100);
    }
    
    /**
     * Obtém resumo do progresso
     */
    getProgressSummary() {
        const finger = this.getCurrentFinger();
        
        return {
            current_finger: finger ? `${finger.hand} - ${finger.name}` : 'Completo',
            progress: `${this.capturedFingers.length}/${this.fingerSequence.length}`,
            percentage: Math.round((this.capturedFingers.length / this.fingerSequence.length) * 100),
            average_quality: this.getAverageQuality(),
            success_rate: this.getSuccessRate(),
            remaining_fingers: this.fingerSequence.length - this.capturedFingers.length
        };
    }
    
    /**
     * Reseta o simulador (para nova tentativa)
     */
    reset() {
        this.currentFingerIndex = 0;
        this.capturedFingers = [];
        this.captureAttempts = [];
        this.activityStartTime = Date.now();
        console.log('[ETAN] Simulador resetado');
    }
}

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.ETANSimulatorManager = ETANSimulatorManager;
}
