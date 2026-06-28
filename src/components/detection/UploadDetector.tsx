import { useRef, useState } from "react";
import { Upload, Loader2, Save } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useSettings } from "@/stores/settingsStore";
import { useHistory } from "@/stores/historyStore";
import { runDetection } from "@/lib/yolo/session";
import { drawDetections } from "@/lib/yolo/draw";
import type { Detection } from "@/lib/yolo/types";
import { CLASS_LABELS } from "@/lib/yolo/types";
import { toast } from "sonner";
import { motion } from "framer-motion";

export function UploadDetector() {
  const inputRef = useRef<HTMLInputElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const settings = useSettings();
  const addHistory = useHistory((s) => s.add);

  const [busy, setBusy] = useState(false);
  const [dets, setDets] = useState<Detection[]>([]);
  const [previewType, setPreviewType] = useState<"image" | "video" | null>(null);
  const [filename, setFilename] = useState("");
  const videoRef = useRef<HTMLVideoElement>(null);

  const handleFile = async (file: File) => {
    setFilename(file.name);
    setDets([]);
    if (file.type.startsWith("image/")) {
      setPreviewType("image");
      await processImage(file);
    } else if (file.type.startsWith("video/")) {
      setPreviewType("video");
      await processVideo(file);
    } else {
      toast.error("Format file tidak didukung");
    }
  };

  const processImage = async (file: File) => {
    setBusy(true);
    try {
      const url = URL.createObjectURL(file);
      const img = new Image();
      img.src = url;
      await img.decode();
      const canvas = canvasRef.current!;
      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      const ctx = canvas.getContext("2d")!;
      ctx.drawImage(img, 0, 0);
      const frame = await runDetection({
        source: img,
        confidence: settings.confidence,
        iou: settings.iou,
        enabledClasses: settings.enabledClasses,
      });
      drawDetections(ctx, frame.detections, { clear: false });
      setDets(frame.detections);

      // Auto-save to history
      const thumbnail = canvas.toDataURL("image/jpeg", 0.7);
      addHistory({
        id: crypto.randomUUID(),
        timestamp: Date.now(),
        source: "image",
        thumbnail,
        detections: frame.detections,
        width: canvas.width,
        height: canvas.height,
      });

      URL.revokeObjectURL(url);
      toast.success(`Selesai: ${frame.detections.length} deteksi — otomatis tersimpan ke riwayat`);
    } catch (e) {
      console.error(e);
      toast.error("Gagal memproses gambar");
    } finally {
      setBusy(false);
    }
  };

  const processVideo = async (file: File) => {
    setBusy(true);
    try {
      const url = URL.createObjectURL(file);
      const v = videoRef.current!;
      v.src = url;
      v.muted = true;
      await v.play();
      const canvas = canvasRef.current!;
      const tick = async () => {
        if (v.paused || v.ended) return;
        if (canvas.width !== v.videoWidth) {
          canvas.width = v.videoWidth;
          canvas.height = v.videoHeight;
        }
        const ctx = canvas.getContext("2d")!;
        ctx.drawImage(v, 0, 0);
        const frame = await runDetection({
          source: v,
          confidence: settings.confidence,
          iou: settings.iou,
          enabledClasses: settings.enabledClasses,
        });
        drawDetections(ctx, frame.detections, { clear: false });
        setDets(frame.detections);
        requestAnimationFrame(() => void tick());
      };
      void tick();
    } catch (e) {
      console.error(e);
      toast.error("Gagal memproses video");
    } finally {
      setBusy(false);
    }
  };

  const saveResult = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    addHistory({
      id: crypto.randomUUID(),
      timestamp: Date.now(),
      source: previewType ?? "image",
      thumbnail: canvas.toDataURL("image/jpeg", 0.7),
      detections: dets,
      width: canvas.width,
      height: canvas.height,
    });
    toast.success("Tersimpan ke riwayat");
  };

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
      <div className="space-y-4">
        <div
          className="grid place-items-center rounded-3xl border-2 border-dashed border-border bg-card/50 p-10 text-center transition hover:bg-card"
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            const f = e.dataTransfer.files?.[0];
            if (f) void handleFile(f);
          }}
        >
          <Upload className="mb-3 h-8 w-8 text-muted-foreground" />
          <p className="text-sm font-medium">Drop gambar atau video di sini</p>
          <p className="text-xs text-muted-foreground">
            JPG, PNG, MP4, WebM — diproses lokal di browser
          </p>
          <Button
            variant="default"
            className="mt-4"
            onClick={() => inputRef.current?.click()}
            disabled={busy}
          >
            {busy ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <Upload className="mr-2 h-4 w-4" />
            )}
            Pilih File
          </Button>
          <input
            ref={inputRef}
            type="file"
            accept="image/*,video/*"
            className="hidden"
            onChange={(e) => {
              const f = e.target.files?.[0];
              if (f) void handleFile(f);
              e.target.value = "";
            }}
          />
        </div>

        <div className="overflow-hidden rounded-3xl border border-border bg-black shadow-elegant">
          <div className="relative aspect-video w-full">
            <video ref={videoRef} className="hidden" playsInline loop muted />
            <canvas ref={canvasRef} className="h-full w-full object-contain" />
            {!filename && (
              <div className="absolute inset-0 grid place-items-center text-sm text-white/60">
                Pratinjau hasil akan tampil di sini
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="space-y-4">
        {filename && (
          <div className="rounded-2xl border border-border bg-card p-4 shadow-soft">
            <p className="truncate text-xs text-muted-foreground">{filename}</p>
            {dets.length > 0 ? (
              <div className="mt-3 flex items-center justify-center gap-2 rounded-lg bg-emerald-500/15 py-2.5 text-sm font-medium text-emerald-400">
                <Save className="h-4 w-4" /> Otomatis tersimpan ke riwayat
              </div>
            ) : (
              <p className="mt-3 text-center text-xs text-muted-foreground">
                Menunggu hasil deteksi...
              </p>
            )}
            <Button
              variant="outline"
              className="mt-2 w-full"
              onClick={saveResult}
              disabled={dets.length === 0}
              size="sm"
            >
              <Save className="mr-2 h-4 w-4" /> Simpan Ulang
            </Button>
          </div>
        )}

        <div className="rounded-2xl border border-border bg-card p-4 shadow-soft">
          <h3 className="mb-3 text-sm font-semibold">Hasil Deteksi</h3>
          {dets.length === 0 ? (
            <p className="text-xs text-muted-foreground">Belum ada deteksi.</p>
          ) : (
            <ul className="space-y-2">
              {dets.map((d, i) => (
                <motion.li
                  key={i}
                  initial={{ opacity: 0, y: 4 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex items-center justify-between rounded-lg bg-secondary px-3 py-2"
                >
                  <span className="flex items-center gap-2 text-sm font-medium">
                    <span
                      className="h-2.5 w-2.5 rounded-full"
                      style={{
                        background:
                          d.className === "mentah"
                            ? "var(--ripe-unripe)"
                            : "var(--ripe-ripe)",
                      }}
                    />
                    {CLASS_LABELS[d.className]}
                  </span>
                  <span className="text-xs text-muted-foreground">
                    {(d.score * 100).toFixed(1)}%
                  </span>
                </motion.li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
