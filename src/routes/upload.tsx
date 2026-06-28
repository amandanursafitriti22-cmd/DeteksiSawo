import { createFileRoute } from "@tanstack/react-router";
import { UploadDetector } from "@/components/detection/UploadDetector";

export const Route = createFileRoute("/upload")({
  head: () => ({
    meta: [
      { title: "Upload Gambar / Video — SawoVision" },
      {
        name: "description",
        content: "Deteksi kematangan buah sawo pada gambar atau video yang diupload.",
      },
    ],
  }),
  component: UploadPage,
});

function UploadPage() {
  return (
    <div className="mx-auto max-w-7xl px-4 py-8 md:px-6 md:py-12">
      <div className="mb-6">
        <h1 className="text-3xl font-bold tracking-tight md:text-4xl">
          Upload Gambar / Video
        </h1>
        <p className="mt-2 text-muted-foreground">
          Pilih file dari perangkatmu — semua diproses lokal.
        </p>
      </div>
      <UploadDetector />
    </div>
  );
}
