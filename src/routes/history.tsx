import { createFileRoute } from "@tanstack/react-router";
import { motion, AnimatePresence } from "framer-motion";
import { Download, FileJson, FileText, Trash2, ImageOff } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { useHistory } from "@/stores/historyStore";
import { downloadJSON, downloadPDF } from "@/lib/export";
import { CLASS_LABELS } from "@/lib/yolo/types";
import { toast } from "sonner";

export const Route = createFileRoute("/history")({
  head: () => ({
    meta: [
      { title: "Riwayat Deteksi — SawoVision" },
      { name: "description", content: "Riwayat deteksi kematangan buah sawo." },
    ],
  }),
  component: HistoryPage,
});

function HistoryPage() {
  const items = useHistory((s) => s.items);
  const remove = useHistory((s) => s.remove);
  const clear = useHistory((s) => s.clear);

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 md:px-6 md:py-12">
      <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-3xl font-bold tracking-tight md:text-4xl">Riwayat</h1>
          <p className="mt-2 text-muted-foreground">
            {items.length} entri tersimpan di perangkat ini.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button
            variant="outline"
            disabled={items.length === 0}
            onClick={() => downloadJSON(items)}
          >
            <FileJson className="mr-2 h-4 w-4" /> Export JSON
          </Button>
          <Button
            variant="outline"
            disabled={items.length === 0}
            onClick={async () => {
              await downloadPDF(items);
              toast.success("PDF berhasil diunduh");
            }}
          >
            <FileText className="mr-2 h-4 w-4" /> Export PDF
          </Button>
          <AlertDialog>
            <AlertDialogTrigger asChild>
              <Button variant="destructive" disabled={items.length === 0}>
                <Trash2 className="mr-2 h-4 w-4" /> Hapus Semua
              </Button>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>Hapus semua riwayat?</AlertDialogTitle>
                <AlertDialogDescription>
                  Tindakan ini tidak dapat dibatalkan.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>Batal</AlertDialogCancel>
                <AlertDialogAction
                  onClick={() => {
                    clear();
                    toast.success("Riwayat dihapus");
                  }}
                >
                  Hapus
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </div>
      </div>

      {items.length === 0 ? (
        <div className="grid place-items-center rounded-3xl border border-dashed border-border bg-card/50 py-24 text-center">
          <ImageOff className="mb-3 h-10 w-10 text-muted-foreground" />
          <p className="font-medium">Belum ada riwayat</p>
          <p className="text-sm text-muted-foreground">
            Lakukan deteksi terlebih dahulu lalu klik "Snap & Simpan".
          </p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <AnimatePresence>
            {items.map((it) => (
              <motion.article
                key={it.id}
                layout
                initial={{ opacity: 0, scale: 0.96 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.96 }}
                className="group overflow-hidden rounded-2xl border border-border bg-card shadow-soft"
              >
                <div className="aspect-video overflow-hidden bg-black">
                  <img
                    src={it.thumbnail}
                    alt="Hasil deteksi"
                    className="h-full w-full object-contain"
                    loading="lazy"
                  />
                </div>
                <div className="space-y-3 p-4">
                  <div className="flex items-center justify-between text-xs text-muted-foreground">
                    <time>
                      {new Date(it.timestamp).toLocaleString("id-ID")}
                    </time>
                    <span className="rounded-full bg-secondary px-2 py-0.5 capitalize">
                      {it.source}
                    </span>
                  </div>
                  <ul className="space-y-1 text-sm">
                    {it.detections.slice(0, 3).map((d, i) => (
                      <li key={i} className="flex items-center justify-between">
                        <span className="flex items-center gap-2">
                          <span
                            className="h-2 w-2 rounded-full"
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
                          {(d.score * 100).toFixed(0)}%
                        </span>
                      </li>
                    ))}
                    {it.detections.length === 0 && (
                      <li className="text-xs text-muted-foreground">
                        Tidak ada objek terdeteksi.
                      </li>
                    )}
                    {it.detections.length > 3 && (
                      <li className="text-xs text-muted-foreground">
                        +{it.detections.length - 3} lagi
                      </li>
                    )}
                  </ul>
                  <div className="flex items-center justify-between pt-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => {
                        const a = document.createElement("a");
                        a.href = it.thumbnail;
                        a.download = `sawo-${it.id}.jpg`;
                        a.click();
                      }}
                    >
                      <Download className="mr-2 h-3.5 w-3.5" /> Unduh
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => remove(it.id)}
                      className="text-destructive hover:text-destructive"
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                </div>
              </motion.article>
            ))}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
}
