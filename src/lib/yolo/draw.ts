import type { Detection } from "./types";
import { CLASS_LABELS } from "./types";

const COLOR_BY_CLASS: Record<string, string> = {
  mentah: "rgb(95,180,90)",
  matang: "rgb(150,90,55)",
};

export function drawDetections(
  ctx: CanvasRenderingContext2D,
  detections: Detection[],
  opts: { mirror?: boolean; clear?: boolean } = {},
) {
  const { canvas } = ctx;
  const shouldClear = opts.clear ?? true;
  if (shouldClear) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
  ctx.save();
  if (opts.mirror) {
    ctx.translate(canvas.width, 0);
    ctx.scale(-1, 1);
  }
  ctx.lineWidth = Math.max(2, canvas.width / 320);
  ctx.font = `${Math.max(14, Math.round(canvas.width / 50))}px ui-sans-serif, system-ui, -apple-system`;
  ctx.textBaseline = "top";

  for (const d of detections) {
    const color = COLOR_BY_CLASS[d.className] ?? "white";
    const { x, y, w, h } = d.bbox;

    // --- Bounding box (drawn in current transform, mirrored or not) ---
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(x, y, w, h, 8);
    ctx.stroke();

    const label = `${CLASS_LABELS[d.className]} ${(d.score * 100).toFixed(0)}%`;
    const padX = 8;
    const padY = 4;
    const textWidth = ctx.measureText(label).width;
    const labelH = parseInt(ctx.font, 10) + padY * 2;
    let labelY = y - labelH;
    if (labelY < 0) labelY = y + 2;

    // Label background (in current transform, aligns with bounding box)
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(x, labelY, textWidth + padX * 2, labelH, 6);
    ctx.fill();

    // --- Label text ---
    ctx.fillStyle = "white";
    if (opts.mirror) {
      // Canvas context is mirrored (translate+scale(-1,1)).
      // We must un-mirror temporarily so the text reads normally.
      ctx.save();
      // Reset to identity
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      // In the mirrored space, the label box left edge (x) corresponds to:
      //   screen_left = canvas.width - (x + textWidth + padX*2)
      // After un-mirroring, draw text at that position.
      const screenX = canvas.width - (x + textWidth + padX * 2);
      ctx.fillText(label, screenX + padX, labelY + padY);
      ctx.restore();
    } else {
      ctx.fillText(label, x + padX, labelY + padY);
    }
  }
  ctx.restore();
}
