import { createFileRoute, Link } from "@tanstack/react-router";
import { motion } from "framer-motion";
import {
  Camera,
  Sparkles,
  Zap,
  ShieldCheck,
  ArrowRight,
  ScanLine,
  BarChart3,
  History,
} from "lucide-react";
import heroImg from "@/assets/hero-sawo.jpg";
import unripe from "@/assets/sawo-unripe.jpg";
import ripe from "@/assets/sawo-ripe.jpg";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "SawoVision — Deteksi Kematangan Buah Sawo Real-Time" },
      {
        name: "description",
        content:
          "Sistem berbasis web untuk klasifikasi kematangan buah sawo (Manilkara zapota) secara real-time dengan YOLOv11.",
      },
      { property: "og:image", content: "/og-hero.jpg" },
    ],
  }),
  component: Landing,
});

function Landing() {
  return (
    <div>
      {/* HERO */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-soft" aria-hidden />
        <div className="absolute inset-0 opacity-[0.07]" aria-hidden>
          <div
            className="absolute -left-32 top-10 h-72 w-72 rounded-full"
            style={{ background: "radial-gradient(closest-side, var(--primary), transparent)" }}
          />
          <div
            className="absolute right-0 top-40 h-96 w-96 rounded-full"
            style={{ background: "radial-gradient(closest-side, var(--accent), transparent)" }}
          />
        </div>

        <div className="relative mx-auto grid max-w-7xl gap-12 px-6 py-16 md:grid-cols-2 md:items-center md:py-24">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="space-y-6"
          >
            <div className="inline-flex items-center gap-2 rounded-full border border-border bg-background/60 px-3 py-1 text-xs backdrop-blur">
              <Sparkles className="h-3.5 w-3.5 text-primary" />
              <span className="font-medium">YOLOv11 · Real-time di Browser</span>
            </div>
            <h1 className="text-balance text-4xl font-bold leading-[1.05] tracking-tight md:text-6xl">
              Deteksi kematangan{" "}
              <span className="bg-gradient-hero bg-clip-text text-transparent">
                buah sawo
              </span>{" "}
              hanya dengan kamera.
            </h1>
            <p className="max-w-xl text-pretty text-base text-muted-foreground md:text-lg">
              Identifikasi otomatis tingkat kematangan{" "}
              <em>mentah</em> dan <em>matang</em> pada
              buah sawo (<i>Manilkara zapota</i>) secara real-time. Model berjalan
              langsung di browser — privasi terjaga, tanpa server.
            </p>
            <div className="flex flex-wrap gap-3">
              <Button asChild size="lg" className="shadow-elegant">
                <Link to="/detect">
                  <Camera className="mr-2 h-4 w-4" /> Mulai Deteksi
                </Link>
              </Button>
              <Button asChild variant="outline" size="lg">
                <Link to="/info">
                  Pelajari kematangan <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </div>
            <dl className="grid max-w-md grid-cols-3 gap-4 pt-4">
              {[
                ["2", "Kelas kematangan"],
                ["≥15", "FPS target"],
                ["100%", "Privat di browser"],
              ].map(([v, l]) => (
                <div key={l} className="rounded-2xl border border-border bg-card/60 p-3 text-center backdrop-blur">
                  <dt className="text-xl font-bold tracking-tight">{v}</dt>
                  <dd className="text-[11px] uppercase tracking-wider text-muted-foreground">{l}</dd>
                </div>
              ))}
            </dl>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.7, delay: 0.1 }}
            className="relative"
          >
            <div className="overflow-hidden rounded-[2rem] border border-border shadow-elegant">
              <img
                src={heroImg}
                alt="Buah sawo dengan beragam tingkat kematangan"
                width={1536}
                height={1024}
                className="h-full w-full object-cover"
              />
            </div>
            <div className="absolute -bottom-4 -left-4 hidden rounded-2xl border border-border bg-card p-3 shadow-elegant md:block">
              <div className="flex items-center gap-3">
                <span className="grid h-9 w-9 place-items-center rounded-xl bg-gradient-hero text-white">
                  <ScanLine className="h-4 w-4" />
                </span>
                <div className="text-xs leading-tight">
                  <div className="font-semibold">YOLOv11 Inference</div>
                  <div className="text-muted-foreground">ONNX Runtime Web</div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* FEATURES */}
      <section className="mx-auto max-w-7xl px-6 py-16 md:py-24">
        <div className="mb-10 max-w-2xl">
          <h2 className="text-3xl font-bold tracking-tight md:text-4xl">
            Dirancang untuk petani, pedagang, dan peneliti.
          </h2>
          <p className="mt-3 text-muted-foreground">
            Antarmuka modern dengan dukungan webcam real-time, upload gambar/video,
            riwayat deteksi, dan dashboard statistik.
          </p>
        </div>

        <div className="grid gap-5 md:grid-cols-3">
          {FEATURES.map((f, i) => (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05 }}
              className="group relative overflow-hidden rounded-3xl border border-border bg-card p-6 shadow-soft transition hover:shadow-elegant"
            >
              <span className="grid h-11 w-11 place-items-center rounded-xl bg-gradient-hero text-white shadow-elegant">
                <f.icon className="h-5 w-5" />
              </span>
              <h3 className="mt-4 text-lg font-semibold">{f.title}</h3>
              <p className="mt-1 text-sm text-muted-foreground">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* RIPENESS PREVIEW */}
      <section className="mx-auto max-w-7xl px-6 pb-16 md:pb-24">
        <div className="mb-8 flex items-end justify-between gap-4">
          <div>
            <h2 className="text-3xl font-bold tracking-tight md:text-4xl">
              Dua kelas kematangan
            </h2>
            <p className="mt-2 text-muted-foreground">
              Mengikuti pedoman dari proposal — ciri visual yang khas tiap tahap.
            </p>
          </div>
          <Button asChild variant="ghost">
            <Link to="/info">
              Lihat semua <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          {[
            { img: unripe, name: "Mentah", color: "var(--ripe-unripe)", desc: "Kulit hijau, keras, getah putih masih banyak." },
            { img: ripe, name: "Matang", color: "var(--ripe-ripe)", desc: "Kulit cokelat sawo, lunak, manis dan beraroma." },
          ].map((c) => (
            <div key={c.name} className="overflow-hidden rounded-3xl border border-border bg-card shadow-soft">
              <div className="aspect-[4/3] overflow-hidden">
                <img src={c.img} alt={c.name} className="h-full w-full object-cover transition duration-500 hover:scale-105" loading="lazy" />
              </div>
              <div className="space-y-2 p-5">
                <span className="inline-flex items-center gap-2 rounded-full bg-secondary px-3 py-1 text-xs font-semibold">
                  <span className="h-2 w-2 rounded-full" style={{ background: c.color }} />
                  {c.name}
                </span>
                <p className="text-sm text-muted-foreground">{c.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto max-w-7xl px-6 pb-24">
        <div className="overflow-hidden rounded-3xl bg-gradient-hero p-10 text-center text-white shadow-elegant md:p-16">
          <h2 className="text-3xl font-bold tracking-tight md:text-4xl">
            Siap mencoba langsung?
          </h2>
          <p className="mx-auto mt-3 max-w-xl text-white/85">
            Aktifkan kamera dan lihat sistem mengenali kematangan buah sawo dalam
            hitungan milidetik.
          </p>
          <div className="mt-6">
            <Button asChild size="lg" variant="secondary" className="shadow-soft">
              <Link to="/detect">
                <Camera className="mr-2 h-4 w-4" /> Buka Live Detection
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}

const FEATURES = [
  {
    title: "Live Webcam Detection",
    desc: "Akses kamera real-time dengan bounding box, label, dan confidence score di overlay canvas.",
    icon: Camera,
  },
  {
    title: "Inference Cepat di Browser",
    desc: "ONNX Runtime Web menjalankan YOLOv11 lokal — tidak ada frame yang dikirim ke server.",
    icon: Zap,
  },
  {
    title: "Privasi Terjaga",
    desc: "Semua data, gambar, dan riwayat tersimpan hanya di perangkat kamu.",
    icon: ShieldCheck,
  },
  {
    title: "Riwayat & Export",
    desc: "Simpan hasil deteksi, lalu unduh sebagai JSON atau laporan PDF rapi.",
    icon: History,
  },
  {
    title: "Dashboard Statistik",
    desc: "Visualisasi distribusi kelas, deteksi harian, dan kelas dominan.",
    icon: BarChart3,
  },
  {
    title: "Pengaturan Lengkap",
    desc: "Atur confidence threshold, IoU, kelas aktif, dark mode, dan kamera.",
    icon: Sparkles,
  },
];
