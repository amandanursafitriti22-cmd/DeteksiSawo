import { useEffect, useRef, useState } from "react";
import { Camera, CameraOff, Loader2, Save, Pause, Play } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useSettings } from "@/stores/settingsStore";
import { useHistory } from "@/stores/historyStore";
import { runDetection, getSession, isModelAvailable } from "@/lib/yolo/session";
import { drawDetections } from "@/lib/yolo/draw";
import type { Detection } from "@/lib/yolo/types";
import { CLASS_LABELS } from "@/lib/yolo/types";
import { toast } from "sonner";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

const AUTO_SAVE_INTERVAL_MS = 8_000; // auto-save every 8 seconds

// Frame skipping: run inference setiap 3 frame saja (bukan tiap frame)
// Ini memungkinkan video render di 60 FPS sementara inference ~20 FPS
const INFERENCE_FRAME_INTERVAL = 3;

export function WebcamDetector() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const rafRef = useRef<number | null>(null);
  const lastTimesRef = useRef<number[]>([]);
  const runningRef = useRef(false);
  const inFlightRef = useRef(false);
  const lastDetsRef = useRef<Detection[]>([]);
  const lastAutoSaveRef = useRef(0);
  const frameCountRef = useRef(0); // For frame skipping optimization

  const [active, setActive] = useState(false);
  const [paused, setPaused] = useState(false);
  const [loadingModel, setLoadingModel] = useState(true);
  const [modelReady, setModelReady] = useState<boolean | null>(null);
  const [fps, setFps] = useState(0);
  const [inferenceMs, setInferenceMs] = useState(0);
  const [dets, setDets] = useState<Detection[]>([]);
  const [autoSaveCount, setAutoSaveCount] = useState(0);

  const settings = useSettings();
  const addHistory = useHistory((s) => s.add);

  /** Capture current video frame + detections as a HistoryItem and save */
  const captureSnapshot = (label?: string) => {
    const video = videoRef.current;
    if (!video || video.readyState < 2 || lastDetsRef.current.length === 0) return;
    const tmp = document.createElement("canvas");
    tmp.width = video.videoWidth;
    tmp.height = video.videoHeight;
    const ctx = tmp.getContext("2d")!;
    // Always save un-mirrored frame so bounding boxes align correctly
    // (mirror is only a CSS visual aid during live viewing)
    ctx.drawImage(video, 0, 0);
    drawDetections(ctx, lastDetsRef.current, { clear: false });
    const thumbnail = tmp.toDataURL("image/jpeg", 0.7);
    addHistory({
      id: crypto.randomUUID(),
      timestamp: Date.now(),
      source: "webcam",
      thumbnail,
      detections: lastDetsRef.current,
      width: tmp.width,
      height: tmp.height,
    });
    setAutoSaveCount((c) => c + 1);
    if (label) {
      toast.success(label, {
        description: `${lastDetsRef.current.length} deteksi`,
      });
    }
  };

  // Lazy-load model status
  useEffect(() => {
    let mounted = true;
    getSession().then(() => {
      if (!mounted) return;
      setLoadingModel(false);
      setModelReady(isModelAvailable());
    });
    return () => {
      mounted = false;
    };
  }, []);

  const stop = () => {
    // Auto-save final snapshot on stop
    captureSnapshot("Sesi selesai — tersimpan ke riwayat");
    runningRef.current = false;
    if (rafRef.current) cancelAnimationFrame(rafRef.current);
    rafRef.current = null;
    streamRef.current?.getTracks().forEach((t) => t.stop());
    streamRef.current = null;
    setActive(false);
    setPaused(false);
    setAutoSaveCount(0);
    lastAutoSaveRef.current = 0;
    frameCountRef.current = 0; // Reset frame counter
    if (canvasRef.current) {
      const ctx = canvasRef.current.getContext("2d");
      ctx?.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    }
  };

  const start = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: settings.cameraId
          ? { deviceId: { exact: settings.cameraId } }
          : { facingMode: "environment", width: { ideal: 1280 } },
        audio: false,
      });
      streamRef.current = stream;
      const video = videoRef.current!;
      video.srcObject = stream;
      await video.play();
      setActive(true);
      runningRef.current = true;
      loop();
    } catch (e) {
      console.error(e);
      toast.error("Gagal mengakses kamera", {
        description: "Pastikan izin kamera diberikan.",
      });
    }
  };

  const loop = () => {
    if (!runningRef.current) return;
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas || video.readyState < 2 || paused) {
      rafRef.current = requestAnimationFrame(loop);
      return;
    }
    if (canvas.width !== video.videoWidth) {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
    }

    // Determine if this frame should run inference
    const shouldRunInference = frameCountRef.current % INFERENCE_FRAME_INTERVAL === 0;
    frameCountRef.current++;

    // Always draw detections at 60 FPS
    const ctx = canvas.getContext("2d")!;
    drawDetections(ctx, lastDetsRef.current, { mirror: settings.mirror });

    // Launch inference in background (non-blocking) on specific frames
    if (!inFlightRef.current && shouldRunInference) {
      inFlightRef.current = true;
      
      // Use Promise.then() instead of async/await to prevent loop blocking
      runDetection({
        source: video,
        confidence: settings.confidence,
        iou: settings.iou,
        enabledClasses: settings.enabledClasses,
      })
        .then((frame) => {
          lastDetsRef.current = frame.detections;
          setDets(frame.detections);
          setInferenceMs(frame.inferenceMs);

          const now = performance.now();
          lastTimesRef.current.push(now);
          lastTimesRef.current = lastTimesRef.current.filter((t) => now - t < 1000);
          setFps(lastTimesRef.current.length);

          // Auto-save periodically when detections exist
          const nowMs = Date.now();
          if (
            frame.detections.length > 0 &&
            nowMs - lastAutoSaveRef.current >= AUTO_SAVE_INTERVAL_MS
          ) {
            lastAutoSaveRef.current = nowMs;
            captureSnapshot();
          }
        })
        .catch((e) => console.error("[detect]", e))
        .finally(() => {
          inFlightRef.current = false;
        });
    }

    rafRef.current = requestAnimationFrame(loop);
  };

  useEffect(() => {
    return () => stop();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const snapAndSave = () => {
    captureSnapshot("Tersimpan ke riwayat");
  };

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
      <div className="relative overflow-hidden rounded-3xl border border-border bg-black shadow-elegant">
        <div
          className={cn(
            "relative aspect-video w-full",
            settings.mirror && active && "[&_video]:scale-x-[-1]",
          )}
        >
          <video
            ref={videoRef}
            playsInline
            muted
            className="h-full w-full object-cover"
            aria-label="Tampilan kamera"
          />
          <canvas
            ref={canvasRef}
            className="pointer-events-none absolute inset-0 h-full w-full"
          />
          {!active && (
            <div className="absolute inset-0 grid place-items-center bg-gradient-to-br from-black/80 to-black/40 text-center text-white">
              <div className="max-w-sm space-y-3 px-6">
                <Camera className="mx-auto h-10 w-10 opacity-80" />
                <h3 className="text-lg font-semibold">Siap mendeteksi</h3>
                <p className="text-sm opacity-80">
                  Klik tombol di bawah untuk mengaktifkan kamera. Inference berjalan
                  100% di browser.
                </p>
                <Button onClick={start} size="lg" className="mt-2">
                  <Camera className="mr-2 h-4 w-4" /> Mulai Kamera
                </Button>
              </div>
            </div>
          )}
        </div>

        {/* HUD */}
        {active && (
          <div className="pointer-events-none absolute left-3 top-3 flex items-center gap-2">
            <Badge className="pointer-events-auto bg-black/60 text-white backdrop-blur">
              <span className="mr-1 inline-block h-2 w-2 animate-pulse rounded-full bg-red-500" />
              LIVE
            </Badge>
            <Badge variant="secondary" className="bg-black/60 text-white backdrop-blur">
              {fps} FPS
            </Badge>
            <Badge variant="secondary" className="bg-black/60 text-white backdrop-blur">
              {inferenceMs.toFixed(0)} ms
            </Badge>
            <Badge
              variant="secondary"
              className="bg-black/60 text-white backdrop-blur"
              title={modelReady ? "best.onnx aktif" : "Mode demo (model belum diunggah)"}
            >
              {modelReady === null
                ? "memuat…"
                : modelReady
                  ? "Model: best.onnx"
                  : "Mode Demo"}
            </Badge>
            {autoSaveCount > 0 && (
              <Badge variant="secondary" className="bg-emerald-600/80 text-white backdrop-blur">
                <Save className="mr-1 h-3 w-3" /> {autoSaveCount} tersimpan
              </Badge>
            )}
          </div>
        )}
      </div>

      <div className="space-y-4">
        <div className="rounded-2xl border border-border bg-card p-4 shadow-soft">
          <h3 className="mb-3 text-sm font-semibold">Kontrol</h3>
          <div className="flex flex-wrap gap-2">
            {!active ? (
              <Button onClick={start} disabled={loadingModel} className="flex-1">
                {loadingModel ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <Camera className="mr-2 h-4 w-4" />
                )}
                Mulai
              </Button>
            ) : (
              <>
                <Button variant="secondary" onClick={() => setPaused((p) => !p)}>
                  {paused ? (
                    <Play className="mr-2 h-4 w-4" />
                  ) : (
                    <Pause className="mr-2 h-4 w-4" />
                  )}
                  {paused ? "Lanjut" : "Jeda"}
                </Button>
                <Button variant="destructive" onClick={stop}>
                  <CameraOff className="mr-2 h-4 w-4" /> Stop
                </Button>
                <Button variant="default" onClick={snapAndSave} className="w-full">
                  <Save className="mr-2 h-4 w-4" /> Snap & Simpan
                </Button>
              </>
            )}
          </div>
          {modelReady === false && (
            <p className="mt-3 rounded-lg bg-secondary p-3 text-xs text-muted-foreground">
              Model <code>best.onnx</code> belum ditemukan di{" "}
              <code>/public/models/</code>. Saat ini sistem menjalankan{" "}
              <strong>mode demo</strong>. Lihat README untuk cara meng-export model.
            </p>
          )}
        </div>

        <div className="rounded-2xl border border-border bg-card p-4 shadow-soft">
          <h3 className="mb-3 text-sm font-semibold">Deteksi saat ini</h3>
          {dets.length === 0 ? (
            <p className="text-xs text-muted-foreground">
              Belum ada buah sawo terdeteksi. Arahkan kamera ke buah.
            </p>
          ) : (
            <ul className="space-y-2">
              {dets.map((d, i) => (
                <motion.li
                  key={i}
                  initial={{ opacity: 0, x: -8 }}
                  animate={{ opacity: 1, x: 0 }}
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
