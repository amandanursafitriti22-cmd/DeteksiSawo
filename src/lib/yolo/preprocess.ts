export interface PreprocessResult {
  tensor: Float32Array;
  scale: number;
  padX: number;
  padY: number;
  modelSize: number;
}

// Reuse single canvas for all preprocessing instead of creating new one each frame
let preprocessCanvas: HTMLCanvasElement | null = null;

function getPreprocessCanvas(modelSize: number): HTMLCanvasElement {
  if (!preprocessCanvas || preprocessCanvas.width !== modelSize || preprocessCanvas.height !== modelSize) {
    preprocessCanvas = document.createElement("canvas");
    preprocessCanvas.width = modelSize;
    preprocessCanvas.height = modelSize;
  }
  return preprocessCanvas;
}

/**
 * Letterbox source image to modelSize x modelSize, normalize to [0,1], NCHW.
 * Returns tensor + transform info to map detections back.
 * 
 * OPTIMIZED: Reuses canvas, minimizes allocations
 */
export function preprocess(
  source: HTMLVideoElement | HTMLImageElement | HTMLCanvasElement,
  modelSize = 640,
): PreprocessResult {
  const sw =
    source instanceof HTMLVideoElement
      ? source.videoWidth
      : source instanceof HTMLImageElement
      ? source.naturalWidth
      : source.width;
  const sh =
    source instanceof HTMLVideoElement
      ? source.videoHeight
      : source instanceof HTMLImageElement
      ? source.naturalHeight
      : source.height;

  const scale = Math.min(modelSize / sw, modelSize / sh);
  const newW = Math.round(sw * scale);
  const newH = Math.round(sh * scale);
  const padX = Math.floor((modelSize - newW) / 2);
  const padY = Math.floor((modelSize - newH) / 2);

  // Reuse canvas for better performance
  const canvas = getPreprocessCanvas(modelSize);
  const ctx = canvas.getContext("2d", { willReadFrequently: true })!;
  
  // Clear and fill
  ctx.fillStyle = "rgb(114,114,114)";
  ctx.fillRect(0, 0, modelSize, modelSize);
  
  // Draw source image
  ctx.drawImage(source, padX, padY, newW, newH);
  
  // Get image data
  const { data } = ctx.getImageData(0, 0, modelSize, modelSize);

  // Convert to normalized tensor (NCHW format)
  const tensor = new Float32Array(3 * modelSize * modelSize);
  const area = modelSize * modelSize;
  
  for (let i = 0; i < area; i++) {
    const r = data[i * 4] / 255;
    const g = data[i * 4 + 1] / 255;
    const b = data[i * 4 + 2] / 255;
    tensor[i] = r;
    tensor[i + area] = g;
    tensor[i + 2 * area] = b;
  }

  return { tensor, scale, padX, padY, modelSize };
}
