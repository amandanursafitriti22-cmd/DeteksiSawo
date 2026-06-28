import { create } from "zustand";
import { persist } from "zustand/middleware";
import { CLASS_NAMES, type ClassName } from "@/lib/yolo/types";

export type ThemeMode = "light" | "dark" | "system";

interface SettingsState {
  confidence: number;
  iou: number;
  enabledClasses: Record<ClassName, boolean>;
  theme: ThemeMode;
  mirror: boolean;
  cameraId: string | null;
  setConfidence: (v: number) => void;
  setIou: (v: number) => void;
  toggleClass: (name: ClassName) => void;
  setTheme: (m: ThemeMode) => void;
  setMirror: (v: boolean) => void;
  setCameraId: (id: string | null) => void;
}

export const useSettings = create<SettingsState>()(
  persist(
    (set) => ({
      confidence: 0.35,
      iou: 0.45,
      enabledClasses: Object.fromEntries(CLASS_NAMES.map((n) => [n, true])) as Record<
        ClassName,
        boolean
      >,
      theme: "system",
      mirror: true,
      cameraId: null,
      setConfidence: (v) => set({ confidence: v }),
      setIou: (v) => set({ iou: v }),
      toggleClass: (name) =>
        set((s) => ({
          enabledClasses: { ...s.enabledClasses, [name]: !s.enabledClasses[name] },
        })),
      setTheme: (m) => set({ theme: m }),
      setMirror: (v) => set({ mirror: v }),
      setCameraId: (id) => set({ cameraId: id }),
    }),
    {
      name: "sawo-settings",
      version: 1,
      merge: (persistedState, currentState) => {
        const p = persistedState as Partial<SettingsState> & {
          enabledClasses?: Record<string, boolean>;
        };
        const c = currentState as SettingsState;

        const enabledFromPersisted = (p.enabledClasses ?? {}) as Record<string, boolean>;
        const enabledClasses: Record<ClassName, boolean> = {
          ...(c.enabledClasses as Record<ClassName, boolean>),
          ...(enabledFromPersisted as Record<ClassName, boolean>),
        };

        const legacyBelumMatang = enabledFromPersisted["belum_matang"];
        if (typeof legacyBelumMatang === "boolean" && enabledFromPersisted["mentah"] === undefined) {
          enabledClasses.mentah = legacyBelumMatang;
        }

        return {
          ...c,
          ...p,
          enabledClasses,
        };
      },
    },
  ),
);
