export type ClassId = 0 | 1;

// Class order MUST match Label Studio export (0=matang, 1=mentah)
export const CLASS_NAMES = ["matang", "mentah"] as const;
export type ClassName = (typeof CLASS_NAMES)[number];

export const CLASS_LABELS: Record<ClassName, string> = {
  matang: "Matang",
  mentah: "Mentah",
};

export const CLASS_COLOR_VAR: Record<ClassName, string> = {
  matang: "var(--ripe-ripe)",
  mentah: "var(--ripe-unripe)",
};

export interface BBox {
  x: number;
  y: number;
  w: number;
  h: number;
}

export interface Detection {
  bbox: BBox;
  classId: ClassId;
  className: ClassName;
  score: number;
}

export interface DetectionFrame {
  detections: Detection[];
  inferenceMs: number;
  width: number;
  height: number;
}

export type DetectionSource = "webcam" | "image" | "video";

export interface HistoryItem {
  id: string;
  timestamp: number;
  source: DetectionSource;
  thumbnail: string; // dataURL
  detections: Detection[];
  width: number;
  height: number;
}

/**
 * Format detection label with confidence score (1-100)
 * Example: "matang 92" or "mentah 85"
 */
export function formatDetectionLabel(detection: Detection): string {
  const confidence = Math.round(detection.score * 100);
  
  // Map internal names to display names for Indonesian
  const displayNames: Record<ClassName, string> = {
    matang: "matang",
    mentah: "mentah",
  };
  
  return `${displayNames[detection.className]} ${confidence}`;
}

/**
 * Get detailed label with display name and confidence
 */
export function getDetectionDisplayLabel(detection: Detection): string {
  const confidence = Math.round(detection.score * 100);
  return `${CLASS_LABELS[detection.className]} (${confidence}%)`;
}
