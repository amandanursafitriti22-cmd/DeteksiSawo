import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useSettings } from "@/stores/settingsStore";
import { CLASS_LABELS, CLASS_NAMES } from "@/lib/yolo/types";
import { Camera, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

export const Route = createFileRoute("/settings")({
  head: () => ({
    meta: [
      { title: "Pengaturan — SawoVision" },
      { name: "description", content: "Atur threshold dan preferensi deteksi." },
    ],
  }),
  component: SettingsPage,
});

function SettingsPage() {
  const s = useSettings();
  const [cams, setCams] = useState<MediaDeviceInfo[]>([]);

  const refreshCams = async () => {
    try {
      // Need permission to read labels; request lightweight stream then stop
      try {
        const tmp = await navigator.mediaDevices.getUserMedia({ video: true });
        tmp.getTracks().forEach((t) => t.stop());
      } catch {
        /* ignore */
      }
      const list = await navigator.mediaDevices.enumerateDevices();
      setCams(list.filter((d) => d.kind === "videoinput"));
    } catch (e) {
      console.error(e);
      toast.error("Gagal memuat daftar kamera");
    }
  };

  useEffect(() => {
    void refreshCams();
  }, []);

  return (
    <div className="mx-auto max-w-3xl px-4 py-8 md:px-6 md:py-12">
      <div className="mb-6">
        <h1 className="text-3xl font-bold tracking-tight md:text-4xl">Pengaturan</h1>
        <p className="mt-2 text-muted-foreground">
          Tersimpan otomatis di perangkat ini.
        </p>
      </div>

      <div className="space-y-5">
        <Section title="Threshold Deteksi" desc="Atur sensitivitas model.">
          <Field label={`Confidence threshold — ${s.confidence.toFixed(2)}`}>
            <Slider
              value={[s.confidence]}
              min={0.1}
              max={0.95}
              step={0.05}
              onValueChange={([v]) => s.setConfidence(v)}
            />
          </Field>
          <Field label={`IoU threshold (NMS) — ${s.iou.toFixed(2)}`}>
            <Slider
              value={[s.iou]}
              min={0.1}
              max={0.9}
              step={0.05}
              onValueChange={([v]) => s.setIou(v)}
            />
          </Field>
        </Section>

        <Section title="Kelas Aktif" desc="Sembunyikan kelas tertentu dari hasil.">
          <div className="space-y-3">
            {CLASS_NAMES.map((n) => (
              <div key={n} className="flex items-center justify-between">
                <Label htmlFor={`cls-${n}`} className="flex items-center gap-2">
                  <span
                    className="h-2.5 w-2.5 rounded-full"
                    style={{
                      background:
                        n === "mentah"
                          ? "var(--ripe-unripe)"
                          : "var(--ripe-ripe)",
                    }}
                  />
                  {CLASS_LABELS[n]}
                </Label>
                <Switch
                  id={`cls-${n}`}
                  checked={s.enabledClasses[n]}
                  onCheckedChange={() => s.toggleClass(n)}
                />
              </div>
            ))}
          </div>
        </Section>

        <Section title="Kamera" desc="Pilih perangkat dan orientasi.">
          <Field label="Perangkat kamera">
            <div className="flex gap-2">
              <Select
                value={s.cameraId ?? "auto"}
                onValueChange={(v) => s.setCameraId(v === "auto" ? null : v)}
              >
                <SelectTrigger className="flex-1">
                  <SelectValue placeholder="Pilih kamera" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="auto">Otomatis</SelectItem>
                  {cams.map((c) => (
                    <SelectItem key={c.deviceId} value={c.deviceId}>
                      {c.label || `Kamera ${c.deviceId.slice(0, 6)}`}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Button variant="outline" size="icon" onClick={refreshCams} aria-label="Muat ulang">
                <RefreshCw className="h-4 w-4" />
              </Button>
            </div>
          </Field>
          <div className="flex items-center justify-between">
            <Label htmlFor="mirror" className="flex items-center gap-2">
              <Camera className="h-4 w-4" /> Mirror tampilan kamera
            </Label>
            <Switch
              id="mirror"
              checked={s.mirror}
              onCheckedChange={(v) => s.setMirror(v)}
            />
          </div>
        </Section>

        <Section title="Tampilan" desc="Pilih mode terang atau gelap.">
          <Field label="Mode tema">
            <Select value={s.theme} onValueChange={(v) => s.setTheme(v as never)}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="system">Mengikuti sistem</SelectItem>
                <SelectItem value="light">Light</SelectItem>
                <SelectItem value="dark">Dark</SelectItem>
              </SelectContent>
            </Select>
          </Field>
        </Section>
      </div>
    </div>
  );
}

function Section({
  title,
  desc,
  children,
}: {
  title: string;
  desc?: string;
  children: React.ReactNode;
}) {
  return (
    <section className="rounded-3xl border border-border bg-card p-6 shadow-soft">
      <header className="mb-4">
        <h2 className="text-base font-semibold">{title}</h2>
        {desc && <p className="text-sm text-muted-foreground">{desc}</p>}
      </header>
      <div className="space-y-4">{children}</div>
    </section>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="space-y-2">
      <Label className="text-sm">{label}</Label>
      {children}
    </div>
  );
}
