import { Link, useLocation } from "@tanstack/react-router";
import { motion } from "framer-motion";
import { Camera, History, Home, Info, LayoutDashboard, Settings, Upload, Leaf } from "lucide-react";
import { cn } from "@/lib/utils";
import { ThemeToggle } from "./ThemeToggle";

const NAV = [
  { to: "/", label: "Beranda", icon: Home },
  { to: "/detect", label: "Deteksi", icon: Camera },
  { to: "/upload", label: "Upload", icon: Upload },
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/history", label: "Riwayat", icon: History },
  { to: "/info", label: "Info", icon: Info },
  { to: "/settings", label: "Setting", icon: Settings },
] as const;

export function Navbar() {
  const { pathname } = useLocation();
  return (
    <header className="sticky top-0 z-40 w-full border-b border-border/60 bg-background/70 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 md:px-6">
        <Link to="/" className="group flex items-center gap-2">
          <span className="grid h-9 w-9 place-items-center rounded-xl bg-gradient-hero text-white shadow-elegant transition group-hover:scale-105">
            <Leaf className="h-5 w-5" aria-hidden />
          </span>
          <div className="leading-tight">
            <div className="text-sm font-bold tracking-tight">SawoVision</div>
            <div className="text-[10px] uppercase tracking-widest text-muted-foreground">
              YOLOv11 · Real-time
            </div>
          </div>
        </Link>

        <nav className="hidden items-center gap-1 md:flex">
          {NAV.map((item) => {
            const active =
              item.to === "/" ? pathname === "/" : pathname.startsWith(item.to);
            return (
              <Link
                key={item.to}
                to={item.to}
                className={cn(
                  "relative rounded-full px-3 py-1.5 text-sm font-medium text-muted-foreground transition hover:text-foreground",
                  active && "text-foreground",
                )}
              >
                {active && (
                  <motion.span
                    layoutId="nav-active"
                    className="absolute inset-0 rounded-full bg-secondary"
                    transition={{ type: "spring", stiffness: 380, damping: 30 }}
                  />
                )}
                <span className="relative">{item.label}</span>
              </Link>
            );
          })}
        </nav>

        <ThemeToggle />
      </div>
    </header>
  );
}

export function BottomNav() {
  const { pathname } = useLocation();
  return (
    <nav
      className="fixed inset-x-0 bottom-0 z-40 border-t border-border/60 bg-background/85 backdrop-blur-xl md:hidden"
      aria-label="Navigasi utama"
    >
      <ul className="mx-auto grid max-w-md grid-cols-7 px-1 py-1.5">
        {NAV.map((item) => {
          const Icon = item.icon;
          const active =
            item.to === "/" ? pathname === "/" : pathname.startsWith(item.to);
          return (
            <li key={item.to} className="contents">
              <Link
                to={item.to}
                className={cn(
                  "flex flex-col items-center gap-0.5 rounded-lg py-1.5 text-[10px] transition",
                  active
                    ? "text-primary"
                    : "text-muted-foreground hover:text-foreground",
                )}
              >
                <Icon className="h-5 w-5" aria-hidden />
                <span className="leading-none">{item.label}</span>
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
