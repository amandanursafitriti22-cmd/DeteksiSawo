import * as ort from "onnxruntime-web";
import { preprocess } from "./preprocess";
import { postprocess } from "./postprocess";
import type { Detection, ClassName, DetectionFrame, ClassId } from "./types";
import { CLASS_NAMES } from "./types";

const MODEL_URL = "/models/best.onnx";

/**
 * Model input size — MUST match the imgsz used during ONNX export.
 * WARNING: Jika tidak sesuai, deteksi error!
 * 
 * Pastikan ini match dengan saat export:
 * yolo export model=best.pt format=onnx imgsz=??? opset=14 simplify=True
 */
const MODEL_SIZE = 512;

let sessionPromise: Promise<ort.InferenceSession | null> | null = null;
let modelAvailable: boolean | null = null;

export type ModelStatus = "loading" | "ready" | "missing" | "error";

export async function getSession(): Promise<ort.InferenceSession | null> {
  if (sessionPromise) return sessionPromise;
  sessionPromise = (async () => {
    try {
      // Quick HEAD check to detect missing model gracefully
      const head = await fetch(MODEL_URL, { method: "HEAD" });
      if (!head.ok) {
        modelAvailable = false;
        return null;
      }

      // Configure WASM for optimal performance
      ort.env.wasm.wasmPaths =
        "https://cdn.jsdelivr.net/npm/onnxruntime-web@1.26.0/dist/";
      ort.env.wasm.numThreads = navigator.hardwareConcurrency || 4;

      // Try WebGL first (GPU-accelerated), fallback to optimized WASM
      let session: ort.InferenceSession;
      try {
        session = await ort.InferenceSession.create(MODEL_URL, {
          executionProviders: ["webgl"],
          graphOptimizationLevel: "all",
        });
        console.log("[yolo] Using WebGL backend (GPU)");
      } catch {
        console.log("[yolo] WebGL unavailable, using WASM backend (CPU)");
        session = await ort.InferenceSession.create(MODEL_URL, {
          executionProviders: ["wasm"],
          graphOptimizationLevel: "all",
        });
      }

      modelAvailable = true;
      return session;
    } catch (e) {
      console.warn("[yolo] model load failed, falling back to dummy:", e);
      modelAvailable = false;
      return null;
    }
  })();
  return sessionPromise;
}

export function isModelAvailable(): boolean | null {
  return modelAvailable;
}

interface RunOpts {
  source: HTMLVideoElement | HTMLImageElement | HTMLCanvasElement;
  confidence: number;
  iou: number;
  enabledClasses: Record<ClassName, boolean>;
}

export async function runDetection(opts: RunOpts): Promise<DetectionFrame> {
  const { source, confidence, iou, enabledClasses } = opts;
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

  const t0 = performance.now();
  const session = await getSession();

  if (!session) {
    // Dummy fallback so UI stays useful while user installs best.onnx
    const dets = dummyDetect(sw, sh, confidence, enabledClasses);
    return {
      detections: dets,
      inferenceMs: performance.now() - t0,
      width: sw,
      height: sh,
    };
  }

  const { tensor, scale, padX, padY, modelSize } = preprocess(source, MODEL_SIZE);
  const inputName = session.inputNames[0];
  const input = new ort.Tensor("float32", tensor, [1, 3, modelSize, modelSize]);
  const result = await session.run({ [inputName]: input });
  const outputName = session.outputNames[0];
  const out = result[outputName];
  const dims = out.dims as number[];
  // Expected [1, 4+nc, anchors]
  const channels = dims[1];
  const anchors = dims[2];
  const detections = postprocess({
    output: out.data as Float32Array,
    channels,
    anchors,
    modelSize,
    scale,
    padX,
    padY,
    origW: sw,
    origH: sh,
    confThr: confidence,
    iouThr: iou,
    enabledClasses,
  });

  return {
    detections,
    inferenceMs: performance.now() - t0,
    width: sw,
    height: sh,
  };
}

// --- Dummy detector ---------------------------------------------------------

let dummyT = 0;

function dummyDetect(
  w: number,
  h: number,
  conf: number,
  enabled: Record<ClassName, boolean>,
): Detection[] {
  dummyT += 0.03;
  const out: Detection[] = [];
  const enabledList = CLASS_NAMES.filter((n) => enabled[n]);
  if (enabledList.length === 0) return out;

  // Generate 1-3 wandering boxes
  const count = 2;
  for (let i = 0; i < count; i++) {
    const cx = w * (0.4 + 0.2 * Math.sin(dummyT + i));
    const cy = h * (0.5 + 0.15 * Math.cos(dummyT * 0.8 + i));
    const bw = w * 0.18;
    const bh = h * 0.22;
    const className = enabledList[i % enabledList.length];
    const classId = CLASS_NAMES.indexOf(className) as ClassId;
    const score = 0.6 + 0.3 * Math.abs(Math.sin(dummyT + i * 1.3));
    if (score < conf) continue;
    out.push({
      bbox: { x: cx - bw / 2, y: cy - bh / 2, w: bw, h: bh },
      classId,
      className,
      score,
    });
  }
  return out;
}
