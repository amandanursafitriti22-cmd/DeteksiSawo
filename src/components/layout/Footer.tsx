import { Link } from "@tanstack/react-router";
import { Github, Leaf } from "lucide-react";

export function Footer() {
  return (
    <footer className="mt-16 border-t border-border/60 bg-background/60 py-8">
      <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-6 text-sm text-muted-foreground md:flex-row">
        <div className="flex items-center gap-2">
          <Leaf className="h-4 w-4 text-primary" aria-hidden />
          <span>SawoVision · YOLOv11 di Browser</span>
        </div>
        <div className="flex items-center gap-4">
          <Link to="/info" className="hover:text-foreground">
            Panduan Kematangan
          </Link>
          <Link to="/settings" className="hover:text-foreground">
            Pengaturan
          </Link>
          <a
            href="https://docs.ultralytics.com/models/yolo11/"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 hover:text-foreground"
          >
            <Github className="h-3.5 w-3.5" /> Ultralytics
          </a>
        </div>
      </div>
    </footer>
  );
}
