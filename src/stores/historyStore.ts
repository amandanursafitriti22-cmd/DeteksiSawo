import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { HistoryItem } from "@/lib/yolo/types";

interface HistoryState {
  items: HistoryItem[];
  add: (item: HistoryItem) => void;
  remove: (id: string) => void;
  clear: () => void;
}

const MAX_ITEMS = 200;

export const useHistory = create<HistoryState>()(
  persist(
    (set) => ({
      items: [],
      add: (item) => set((s) => ({ items: [item, ...s.items].slice(0, MAX_ITEMS) })),
      remove: (id) => set((s) => ({ items: s.items.filter((i) => i.id !== id) })),
      clear: () => set({ items: [] }),
    }),
    { name: "sawo-history" },
  ),
);
