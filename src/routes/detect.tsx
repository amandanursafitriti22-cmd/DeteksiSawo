import { createFileRoute } from "@tanstack/react-router";
import { motion } from "framer-motion";
import { WebcamDetector } from "@/components/detection/WebcamDetector";

export const Route = createFileRoute("/detect")({
  head: () => ({
    meta: [
      { title: "Live Detection — SawoVision" },
      {
        name: "description",
        content: "Deteksi kematangan buah sawo secara real-time melalui webcam.",
      },
    ],
  }),
  component: DetectPage,
});

function DetectPage() {
  return (
    <div className="mx-auto max-w-7xl px-4 py-8 md:px-6 md:py-12">
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-6"
      >
        <h1 className="text-3xl font-bold tracking-tight md:text-4xl">
          Live Detection
        </h1>
        <p className="mt-2 text-muted-foreground">
          Aktifkan kamera, arahkan ke buah sawo, dan biarkan YOLOv11 bekerja.
        </p>
      </motion.div>
      <WebcamDetector />
    </div>
  );
}
