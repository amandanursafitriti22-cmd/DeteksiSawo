import { createFileRoute } from "@tanstack/react-router";
import { motion } from "framer-motion";
import unripe from "@/assets/sawo-unripe.jpg";
import ripe from "@/assets/sawo-ripe.jpg";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export const Route = createFileRoute("/info")({
  head: () => ({
    meta: [
      { title: "Informasi Kematangan Sawo — SawoVision" },
      {
        name: "description",
        content:
          "Panduan visual ciri-ciri kematangan buah sawo (Manilkara zapota).",
      },
    ],
  }),
  component: InfoPage,
});

const DATA = [
  {
    name: "Mentah",
    key: "mentah",
    img: unripe,
    color: "var(--ripe-unripe)",
    skin: "Hijau cerah, halus",
    texture: "Keras saat ditekan",
    aroma: "Tidak beraroma",
    sap: "Banyak getah putih",
    use: "Belum siap konsumsi",
    desc: "Kulit dominan hijau, tekstur permukaan masih halus dan keras. Banyak getah putih saat dipetik. Rasa sepat, belum manis.",
  },
  {
    name: "Matang",
    key: "matang",
    img: ripe,
    color: "var(--ripe-ripe)",
    skin: "Cokelat sawo merata",
    texture: "Lunak saat ditekan halus",
    aroma: "Harum manis khas",
    sap: "Hampir tidak ada",
    use: "Siap dikonsumsi",
    desc: "Kulit cokelat sawo merata, daging buah lunak, sangat manis dan beraroma harum khas. Siap dikonsumsi langsung.",
  },
];

function InfoPage() {
  return (
    <div className="mx-auto max-w-7xl px-4 py-8 md:px-6 md:py-12">
      <div className="mb-8 max-w-2xl">
        <h1 className="text-3xl font-bold tracking-tight md:text-4xl">
          Informasi Kematangan
        </h1>
        <p className="mt-2 text-muted-foreground">
          Ciri visual buah sawo (<i>Manilkara zapota</i>) untuk tiap tahap kematangan,
          mengikuti pedoman dari proposal penelitian.
        </p>
      </div>

      <div className="mb-10 grid gap-5 md:grid-cols-2">
        {DATA.map((d, i) => (
          <motion.article
            key={d.key}
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.06 }}
            className="overflow-hidden rounded-3xl border border-border bg-card shadow-soft"
          >
            <div className="aspect-[4/3] overflow-hidden">
              <img
                src={d.img}
                alt={`Sawo ${d.name}`}
                className="h-full w-full object-cover"
                loading="lazy"
              />
            </div>
            <div className="space-y-3 p-5">
              <span
                className="inline-flex items-center gap-2 rounded-full bg-secondary px-3 py-1 text-xs font-semibold"
              >
                <span className="h-2 w-2 rounded-full" style={{ background: d.color }} />
                {d.name}
              </span>
              <p className="text-sm text-muted-foreground">{d.desc}</p>
            </div>
          </motion.article>
        ))}
      </div>

      <div className="overflow-hidden rounded-3xl border border-border bg-card shadow-soft">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Tahap</TableHead>
              <TableHead>Warna Kulit</TableHead>
              <TableHead>Tekstur</TableHead>
              <TableHead>Aroma</TableHead>
              <TableHead>Getah</TableHead>
              <TableHead>Kegunaan</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {DATA.map((d) => (
              <TableRow key={d.key}>
                <TableCell>
                  <span className="flex items-center gap-2 font-medium">
                    <span
                      className="h-2.5 w-2.5 rounded-full"
                      style={{ background: d.color }}
                    />
                    {d.name}
                  </span>
                </TableCell>
                <TableCell>{d.skin}</TableCell>
                <TableCell>{d.texture}</TableCell>
                <TableCell>{d.aroma}</TableCell>
                <TableCell>{d.sap}</TableCell>
                <TableCell>{d.use}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <div className="mt-8 rounded-2xl border border-border bg-secondary/50 p-5 text-sm text-muted-foreground">
        <p>
          <strong className="text-foreground">Catatan:</strong> Akurasi klasifikasi
          dipengaruhi pencahayaan, sudut pengambilan, dan kualitas kamera. Untuk
          hasil terbaik, foto buah pada pencahayaan alami dengan latar polos.
        </p>
      </div>
    </div>
  );
}
