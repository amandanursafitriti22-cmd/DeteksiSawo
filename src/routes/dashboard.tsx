import { createFileRoute } from "@tanstack/react-router";
import { useMemo } from "react";
import { motion } from "framer-motion";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";
import { useHistory } from "@/stores/historyStore";
import { CLASS_LABELS, CLASS_NAMES, type ClassName } from "@/lib/yolo/types";
import { TrendingUp, ScanLine, Trophy, Clock } from "lucide-react";

export const Route = createFileRoute("/dashboard")({
  head: () => ({
    meta: [
      { title: "Dashboard — SawoVision" },
      { name: "description", content: "Statistik deteksi kematangan buah sawo." },
    ],
  }),
  component: DashboardPage,
});

const COLORS: Record<ClassName, string> = {
  matang: "rgb(150,90,55)",
  mentah: "rgb(95,180,90)",
};

function DashboardPage() {
  const items = useHistory((s) => s.items);

  const stats = useMemo(() => {
    const total = items.reduce((acc, it) => acc + it.detections.length, 0);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const todayItems = items.filter((i) => i.timestamp >= today.getTime());
    const todayCount = todayItems.reduce(
      (acc, it) => acc + it.detections.length,
      0,
    );
    const byClass = Object.fromEntries(
      CLASS_NAMES.map((n) => [n, 0]),
    ) as Record<ClassName, number>;
    items.forEach((it) =>
      it.detections.forEach((d) => {
        byClass[d.className]++;
      }),
    );
    const dominant = (Object.entries(byClass).sort(
      (a, b) => b[1] - a[1],
    )[0]?.[0] ?? "—") as ClassName | "—";

    // Last 7 days
    const days: { day: string; count: number }[] = [];
    for (let i = 6; i >= 0; i--) {
      const d = new Date();
      d.setHours(0, 0, 0, 0);
      d.setDate(d.getDate() - i);
      const next = new Date(d);
      next.setDate(d.getDate() + 1);
      const c = items
        .filter((it) => it.timestamp >= d.getTime() && it.timestamp < next.getTime())
        .reduce((acc, it) => acc + it.detections.length, 0);
      days.push({
        day: d.toLocaleDateString("id-ID", { weekday: "short" }),
        count: c,
      });
    }

    return { total, todayCount, byClass, dominant, days };
  }, [items]);

  const pieData = CLASS_NAMES.map((n) => ({
    name: CLASS_LABELS[n],
    key: n,
    value: stats.byClass[n],
  })).filter((d) => d.value > 0);

  const cards = [
    { label: "Total Deteksi", value: stats.total, icon: ScanLine },
    { label: "Hari Ini", value: stats.todayCount, icon: Clock },
    {
      label: "Kelas Dominan",
      value: stats.dominant === "—" ? "—" : CLASS_LABELS[stats.dominant],
      icon: Trophy,
    },
    { label: "Total Sesi", value: items.length, icon: TrendingUp },
  ];

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 md:px-6 md:py-12">
      <div className="mb-6">
        <h1 className="text-3xl font-bold tracking-tight md:text-4xl">Dashboard</h1>
        <p className="mt-2 text-muted-foreground">
          Ringkasan statistik dari riwayat deteksi.
        </p>
      </div>

      <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map((c, i) => (
          <motion.div
            key={c.label}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.04 }}
            className="rounded-2xl border border-border bg-card p-5 shadow-soft"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
                {c.label}
              </span>
              <c.icon className="h-4 w-4 text-primary" />
            </div>
            <div className="mt-2 truncate text-2xl font-bold">{c.value}</div>
          </motion.div>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-5">
        <div className="rounded-3xl border border-border bg-card p-6 shadow-soft lg:col-span-2">
          <h3 className="mb-4 text-sm font-semibold">Distribusi Kelas</h3>
          {pieData.length === 0 ? (
            <p className="py-12 text-center text-sm text-muted-foreground">
              Belum ada data.
            </p>
          ) : (
            <div className="h-64">
              <ResponsiveContainer>
                <PieChart>
                  <Pie
                    data={pieData}
                    dataKey="value"
                    nameKey="name"
                    innerRadius={50}
                    outerRadius={90}
                    paddingAngle={3}
                  >
                    {pieData.map((d) => (
                      <Cell
                        key={d.key}
                        fill={COLORS[d.key as ClassName]}
                        stroke="var(--card)"
                        strokeWidth={2}
                      />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      borderRadius: 12,
                      border: "1px solid var(--border)",
                      background: "var(--card)",
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          )}
          <ul className="mt-4 space-y-1.5 text-sm">
            {CLASS_NAMES.map((n) => (
              <li key={n} className="flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <span
                    className="h-2.5 w-2.5 rounded-full"
                    style={{ background: COLORS[n] }}
                  />
                  {CLASS_LABELS[n]}
                </span>
                <span className="text-muted-foreground">
                  {stats.byClass[n]}
                </span>
              </li>
            ))}
          </ul>
        </div>

        <div className="rounded-3xl border border-border bg-card p-6 shadow-soft lg:col-span-3">
          <h3 className="mb-4 text-sm font-semibold">Deteksi 7 Hari Terakhir</h3>
          <div className="h-64">
            <ResponsiveContainer>
              <BarChart data={stats.days}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="day" stroke="var(--muted-foreground)" fontSize={12} />
                <YAxis stroke="var(--muted-foreground)" fontSize={12} allowDecimals={false} />
                <Tooltip
                  contentStyle={{
                    borderRadius: 12,
                    border: "1px solid var(--border)",
                    background: "var(--card)",
                  }}
                />
                <Bar dataKey="count" fill="var(--primary)" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
