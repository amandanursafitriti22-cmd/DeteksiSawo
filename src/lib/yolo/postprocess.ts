import type { BBox, ClassId, Detection, ClassName } from "./types";
import { CLASS_NAMES } from "./types";

export interface RawOutput {
  data: Float32Array;
  // YOLOv8/v11 onnx export: shape [1, 4 + nc, N] where nc=3, N=8400 for 640.
  dims: number[];
}

function iou(a: BBox, b: BBox): number {
  const ax2 = a.x + a.w;
  const ay2 = a.y + a.h;
  const bx2 = b.x + b.w;
  const by2 = b.y + b.h;
  const ix1 = Math.max(a.x, b.x);
  const iy1 = Math.max(a.y, b.y);
  const ix2 = Math.min(ax2, bx2);
  const iy2 = Math.min(ay2, by2);
  const iw = Math.max(0, ix2 - ix1);
  const ih = Math.max(0, iy2 - iy1);
  const inter = iw * ih;
  const union = a.w * a.h + b.w * b.h - inter;
  return union <= 0 ? 0 : inter / union;
}

function nms(dets: Detection[], iouThr: number): Detection[] {
  const sorted = [...dets].sort((a, b) => b.score - a.score);
  const keep: Detection[] = [];
  for (const d of sorted) {
    let drop = false;
    for (const k of keep) {
      if (k.classId === d.classId && iou(k.bbox, d.bbox) > iouThr) {
        drop = true;
        break;
      }
    }
    if (!drop) keep.push(d);
  }
  return keep;
}

interface PostprocessOpts {
  output: Float32Array;
  // [batch, channels, anchors] e.g. [1, 7, 8400]
  channels: number;
  anchors: number;
  modelSize: number; // 640
  // Letterbox info to map back to source image
  scale: number;
  padX: number;
  padY: number;
  origW: number;
  origH: number;
  confThr: number;
  iouThr: number;
  enabledClasses: Record<ClassName, boolean>;
}

export function postprocess(opts: PostprocessOpts): Detection[] {
  const {
    output,
    channels,
    anchors,
    scale,
    padX,
    padY,
    origW,
    origH,
    confThr,
    iouThr,
    enabledClasses,
  } = opts;
  const nc = channels - 4;
  const candidates: Detection[] = [];

  for (let i = 0; i < anchors; i++) {
    // YOLOv8/v11 layout: [cx, cy, w, h, c0, c1, ... cn-1] across channels for each anchor.
    let bestScore = 0;
    let bestCls = 0;
    for (let c = 0; c < nc; c++) {
      const s = output[(4 + c) * anchors + i];
      if (s > bestScore) {
        bestScore = s;
        bestCls = c;
      }
    }
    if (bestScore < confThr) continue;
    if (bestCls >= CLASS_NAMES.length) continue;
    const className = CLASS_NAMES[bestCls];
    if (!enabledClasses[className]) continue;

    const cx = output[0 * anchors + i];
    const cy = output[1 * anchors + i];
    const w = output[2 * anchors + i];
    const h = output[3 * anchors + i];

    // Map from letterboxed model coords back to source image coords
    const x = (cx - w / 2 - padX) / scale;
    const y = (cy - h / 2 - padY) / scale;
    const ww = w / scale;
    const hh = h / scale;

    const bbox: BBox = {
      x: Math.max(0, Math.min(origW, x)),
      y: Math.max(0, Math.min(origH, y)),
      w: Math.max(0, Math.min(origW - x, ww)),
      h: Math.max(0, Math.min(origH - y, hh)),
    };
    if (bbox.w < 2 || bbox.h < 2) continue;

    candidates.push({
      bbox,
      classId: bestCls as ClassId,
      className,
      score: bestScore,
    });
  }

  return nms(candidates, iouThr);
}
