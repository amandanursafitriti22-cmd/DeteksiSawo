import jsPDF from "jspdf";
import type { HistoryItem } from "@/lib/yolo/types";
import { CLASS_LABELS } from "@/lib/yolo/types";

export function downloadJSON(items: HistoryItem[]) {
  const blob = new Blob([JSON.stringify(items, null, 2)], {
    type: "application/json",
  });
  triggerDownload(blob, `sawo-history-${Date.now()}.json`);
}

export async function downloadPDF(items: HistoryItem[]) {
  const doc = new jsPDF({ unit: "pt", format: "a4" });
  const pageW = doc.internal.pageSize.getWidth();
  const margin = 40;
  let y = margin;

  doc.setFont("helvetica", "bold");
  doc.setFontSize(20);
  doc.text("SawoVision — Riwayat Deteksi", margin, y);
  y += 24;
  doc.setFont("helvetica", "normal");
  doc.setFontSize(10);
  doc.text(`Diekspor: ${new Date().toLocaleString("id-ID")}`, margin, y);
  doc.text(`Total: ${items.length} entri`, pageW - margin, y, { align: "right" });
  y += 18;

  for (const item of items) {
    if (y > 720) {
      doc.addPage();
      y = margin;
    }
    const thumbW = 120;
    const thumbH = 90;
    try {
      doc.addImage(item.thumbnail, "JPEG", margin, y, thumbW, thumbH);
    } catch {
      doc.rect(margin, y, thumbW, thumbH);
    }
    const tx = margin + thumbW + 16;
    doc.setFont("helvetica", "bold");
    doc.setFontSize(11);
    doc.text(new Date(item.timestamp).toLocaleString("id-ID"), tx, y + 12);
    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    doc.text(`Sumber: ${item.source}`, tx, y + 28);
    doc.text(`Resolusi: ${item.width}×${item.height}`, tx, y + 42);
    doc.text(`Total deteksi: ${item.detections.length}`, tx, y + 56);

    let dy = y + 72;
    for (const d of item.detections.slice(0, 4)) {
      doc.text(
        `• ${CLASS_LABELS[d.className]} — ${(d.score * 100).toFixed(1)}%`,
        tx,
        dy,
      );
      dy += 12;
    }
    y += Math.max(thumbH, 90) + 18;
  }

  doc.save(`sawo-history-${Date.now()}.pdf`);
}

function triggerDownload(blob: Blob, name: string) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  URL.revokeObjectURL(url);
}
