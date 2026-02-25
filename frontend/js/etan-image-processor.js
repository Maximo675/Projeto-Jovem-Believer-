/**
 * Processador Avançado de Imagens para Simulador ETAN
 * Análises de qualidade biométrica baseadas em processamento de imagem
 * 
 * Compatível com: infant-capture-simulator.html
 */

class ETANImageProcessor {
    constructor(canvasWidth = 250, canvasHeight = 250) {
        this.width = canvasWidth;
        this.height = canvasHeight;
        this.imageHistory = [];
        this.maxHistoryFrames = 10;
    }

    /**
     * Aplicar filtro Gaussian Blur para suavizar a imagem
     */
    gaussianBlur(imageData, radius = 2) {
        const data = imageData.data;
        const width = imageData.width;
        const height = imageData.height;
        const outputData = new Uint8ClampedArray(data);

        // Kernel Gauss simples
        const kernel = [
            [1, 4, 6, 4, 1],
            [4, 16, 24, 16, 4],
            [6, 24, 36, 24, 6],
            [4, 16, 24, 16, 4],
            [1, 4, 6, 4, 1]
        ];
        
        const kernelSum = 256;
        const kernelHalf = Math.floor(kernel.length / 2);

        for (let y = kernelHalf; y < height - kernelHalf; y++) {
            for (let x = kernelHalf; x < width - kernelHalf; x++) {
                let r = 0, g = 0, b = 0;

                for (let ky = 0; ky < kernel.length; ky++) {
                    for (let kx = 0; kx < kernel[ky].length; kx++) {
                        const px = (x + kx - kernelHalf) * 4;
                        const py = (y + ky - kernelHalf) * width * 4;
                        
                        const idx = py + px;
                        r += data[idx] * kernel[ky][kx];
                        g += data[idx + 1] * kernel[ky][kx];
                        b += data[idx + 2] * kernel[ky][kx];
                    }
                }

                const outIdx = (y * width + x) * 4;
                outputData[outIdx] = Math.round(r / kernelSum);
                outputData[outIdx + 1] = Math.round(g / kernelSum);
                outputData[outIdx + 2] = Math.round(b / kernelSum);
                outputData[outIdx + 3] = data[outIdx + 3]; // Alpha
            }
        }

        imageData.data.set(outputData);
        return imageData;
    }

    /**
     * Detecção de bordas usando Sobel
     */
    sobelEdgeDetection(imageData) {
        const data = imageData.data;
        const width = imageData.width;
        const height = imageData.height;
        
        // Converter para escala de cinza
        const grayData = new Uint8ClampedArray(width * height);
        for (let i = 0; i < data.length; i += 4) {
            grayData[i / 4] = (data[i] + data[i + 1] + data[i + 2]) / 3;
        }

        const edgeData = new Uint8ClampedArray(data);
        
        // Kernels Sobel
        const sobelX = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]];
        const sobelY = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]];

        for (let y = 1; y < height - 1; y++) {
            for (let x = 1; x < width - 1; x++) {
                let gx = 0, gy = 0;

                for (let ky = -1; ky <= 1; ky++) {
                    for (let kx = -1; kx <= 1; kx++) {
                        const idx = ((y + ky) * width + (x + kx));
                        gx += grayData[idx] * sobelX[ky + 1][kx + 1];
                        gy += grayData[idx] * sobelY[ky + 1][kx + 1];
                    }
                }

                const magnitude = Math.sqrt(gx * gx + gy * gy);
                const idx = (y * width + x) * 4;
                
                edgeData[idx] = magnitude;
                edgeData[idx + 1] = magnitude;
                edgeData[idx + 2] = magnitude;
                edgeData[idx + 3] = 255;
            }
        }

        return new ImageData(edgeData, width, height);
    }

    /**
     * Análise de Contraste Local
     */
    analyzeLocalContrast(imageData, windowSize = 25) {
        const data = imageData.data;
        const width = imageData.width;
        const height = imageData.height;
        const halfWindow = Math.floor(windowSize / 2);
        
        let totalContrast = 0;
        let contrastRegions = 0;

        for (let y = halfWindow; y < height - halfWindow; y++) {
            for (let x = halfWindow; x < width - halfWindow; x++) {
                let min = 255, max = 0;

                // Análise da janela local
                for (let wy = -halfWindow; wy <= halfWindow; wy++) {
                    for (let wx = -halfWindow; wx <= halfWindow; wx++) {
                        const idx = ((y + wy) * width + (x + wx)) * 4;
                        const brightness = (data[idx] + data[idx + 1] + data[idx + 2]) / 3;
                        
                        min = Math.min(min, brightness);
                        max = Math.max(max, brightness);
                    }
                }

                totalContrast += (max - min);
                contrastRegions++;
            }
        }

        return totalContrast / contrastRegions || 0;
    }

    /**
     * Detecção de Região de Interesse (ROI) do dedo
     */
    detectFingerROI(imageData) {
        const data = imageData.data;
        const width = imageData.width;
        const height = imageData.height;
        
        let minX = width, maxX = 0;
        let minY = height, maxY = 0;
        let pixelCount = 0;

        // Threshold adaptativo para pele/dedo
        const skinThreshold = 150;

        for (let i = 0; i < data.length; i += 4) {
            const r = data[i];
            const g = data[i + 1];
            const b = data[i + 2];
            
            // Detecção de pele (tons de rosa/marrom)
            const isSkin = (r > 95 && g > 40 && b > 20 &&
                           r > g && r > b &&
                           Math.abs(r - g) > 15);
            
            if (isSkin) {
                const pixelIndex = i / 4;
                const x = pixelIndex % width;
                const y = Math.floor(pixelIndex / width);
                
                minX = Math.min(minX, x);
                maxX = Math.max(maxX, x);
                minY = Math.min(minY, y);
                maxY = Math.max(maxY, y);
                pixelCount++;
            }
        }

        const roiWidth = maxX - minX;
        const roiHeight = maxY - minY;
        const roiArea = roiWidth * roiHeight;

        return {
            detected: pixelCount > 0,
            roiX: minX,
            roiY: minY,
            roiWidth: roiWidth,
            roiHeight: roiHeight,
            roiArea: roiArea,
            skinPixelCount: pixelCount,
            confidence: Math.min(100, (pixelCount / (WIDTH * height)) * 200)
        };
    }

    /**
     * Análise NFIQ (Não implementado - requer SDK real)
     * Esta é uma simulação baseada em características visual
     */
    estimateNFIQScore(imageData) {
        const data = imageData.data;
        const width = imageData.width;
        const height = imageData.height;

        // Análise 1: Contraste global
        let minBrightness = 255, maxBrightness = 0;
        let totalBrightness = 0;

        for (let i = 0; i < data.length; i += 4) {
            const brightness = (data[i] + data[i + 1] + data[i + 2]) / 3;
            minBrightness = Math.min(minBrightness, brightness);
            maxBrightness = Math.max(maxBrightness, brightness);
            totalBrightness += brightness;
        }

        const contrastScore = (maxBrightness - minBrightness) / 2.55;
        const avgBrightness = totalBrightness / (data.length / 4);
        const brightnessScore = Math.max(0, 100 - Math.abs(avgBrightness - 127) / 1.27);

        // Análise 2: Definição de bordas
        const edgeData = this.sobelEdgeDetection(imageData);
        let edgeCount = 0;
        for (let i = 0; i < edgeData.data.length; i += 4) {
            if (edgeData.data[i] > 50) edgeCount++;
        }
        const edgeScore = Math.min(100, (edgeCount / (width * height)) * 1000);

        // Análise 3: Uniformidade de superfície
        let variance = 0;
        for (let i = 0; i < data.length; i += 4) {
            const brightness = (data[i] + data[i + 1] + data[i + 2]) / 3;
            variance += Math.pow(brightness - avgBrightness, 2);
        }
        variance = variance / (data.length / 4);
        const uniformityScore = 100 - Math.min(100, variance / 25);

        // Score final ponderado
        const nfiqScore = Math.round(
            (contrastScore * 0.3 +
             edgeScore * 0.4 +
             uniformityScore * 0.2 +
             brightnessScore * 0.1)
        );

        return {
            score: Math.max(0, Math.min(100, nfiqScore)),
            contrastScore: contrastScore,
            edgeScore: edgeScore,
            uniformityScore: uniformityScore,
            brightnessScore: brightnessScore,
            avgBrightness: avgBrightness
        };
    }

    /**
     * Análise de Pressão Estimada
     */
    estimatePressure(imageData) {
        const roi = this.detectFingerROI(imageData);
        
        if (!roi.detected) {
            return 0;
        }

        // Quanto maior a ROI, maior a pressão (teoria simplificada)
        const contactArea = roi.roiArea / (this.width * this.height);
        const estimatedPressure = Math.round(contactArea * 150);

        return Math.min(150, Math.max(0, estimatedPressure));
    }

    /**
     * Análise Completa de Qualidade
     */
    analyzeFrameQuality(imageData) {
        const nfiq = this.estimateNFIQScore(imageData);
        const roi = this.detectFingerROI(imageData);
        const contrast = this.analyzeLocalContrast(imageData);
        const pressure = this.estimatePressure(imageData);

        return {
            nfiqScore: nfiq.score,
            roiDetection: roi,
            localContrast: contrast,
            estimatedPressure: pressure,
            qualityLevel: this.getQualityLevel(nfiq.score),
            details: nfiq
        };
    }

    /**
     * Classificar nível de qualidade
     */
    getQualityLevel(score) {
        if (score >= 80) return 'EXCELENTE';
        if (score >= 60) return 'BOA';
        if (score >= 40) return 'ACEITÁVEL';
        if (score >= 20) return 'FRACA';
        return 'REJEITADA';
    }

    /**
     * Armazenar frame no histórico
     */
    storeFrame(imageData) {
        this.imageHistory.push({
            timestamp: Date.now(),
            imageData: imageData
        });

        if (this.imageHistory.length > this.maxHistoryFrames) {
            this.imageHistory.shift();
        }
    }

    /**
     * Análise de progresso baseada no histórico
     */
    analyzeProgress() {
        if (this.imageHistory.length === 0) return null;

        const scores = this.imageHistory.map(frame => {
            return this.estimateNFIQScore(frame.imageData).score;
        });

        return {
            frames: this.imageHistory.length,
            averageScore: scores.reduce((a, b) => a + b, 0) / scores.length,
            maxScore: Math.max(...scores),
            minScore: Math.min(...scores),
            trend: scores[scores.length - 1] - scores[0],
            isImproving: scores[scores.length - 1] > scores[0]
        };
    }
}

// Exportar para uso global
window.ETANImageProcessor = ETANImageProcessor;

console.log('✅ ETANImageProcessor carregado - Use window.imageProcessor para análises avançadas');
