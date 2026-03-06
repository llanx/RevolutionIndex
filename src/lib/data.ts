/**
 * @file src/lib/data.ts
 * @description DATA CONTRACT — Revolution Index JSON Schema
 *
 * This file defines the TypeScript interfaces that ALL JSON data files must conform to.
 * It is the authoritative schema for:
 *   - public/data/current.json  (CurrentData)
 *   - public/data/history.json  (HistoryData)
 *   - public/data/factors.json  (FactorsData)
 *
 * PIPELINE OBLIGATION: Any future data pipeline (Python, GitHub Actions, etc.)
 * must produce JSON files that match these interfaces exactly.
 * Field names, types, nesting structure, and value ranges are all binding.
 *
 * Zone boundary thresholds (provisional — calibrate when model is built):
 *   0–25:  Stable
 *   26–50: Elevated Tension
 *   51–75: Crisis Territory
 *   76–100: Revolution Territory
 */

// ---------------------------------------------------------------------------
// Shared primitives
// ---------------------------------------------------------------------------

/**
 * Zone label for the revolution probability spectrum.
 * Displayed verbatim in the UI — pipeline must use these exact strings.
 */
export type ZoneLabel =
  | 'Stable'
  | 'Elevated Tension'
  | 'Crisis Territory'
  | 'Revolution Territory';

/**
 * Direction indicator for a factor's current influence on the score.
 * - 'up': factor is actively pushing the composite score higher
 * - 'down': factor is actively pushing the composite score lower
 * - 'neutral': factor is present but not driving movement
 */
export type FactorDirection = 'up' | 'down' | 'neutral';

// ---------------------------------------------------------------------------
// Zone configuration — single source of truth
// ---------------------------------------------------------------------------

/** Zone boundary, color, and label used across the dashboard. */
export interface ZoneConfig {
  start: number;
  end: number;
  label: ZoneLabel;
  /** Hex color for canvas/SVG rendering (D3, Chart.js). */
  color: string;
  /** CSS custom property for HTML element styling. */
  cssVar: string;
}

export const ZONES: ZoneConfig[] = [
  { start: 0,   end: 25,  label: 'Stable',             color: '#40916c', cssVar: 'var(--zone-stable)' },
  { start: 25,  end: 50,  label: 'Elevated Tension',    color: '#f4a261', cssVar: 'var(--zone-elevated)' },
  { start: 50,  end: 75,  label: 'Crisis Territory',    color: '#e76f51', cssVar: 'var(--zone-crisis)' },
  { start: 75,  end: 100, label: 'Revolution Territory', color: '#c1121f', cssVar: 'var(--zone-revolution)' },
];

// ---------------------------------------------------------------------------
// current.json — CurrentData
// ---------------------------------------------------------------------------

/**
 * A single contributing factor as it appears in current.json.
 * Factors are ordered highest-weight-first in the JSON array.
 */
export interface Factor {
  /**
   * Stable machine-readable identifier.
   * Pipeline must use this exact string — it is used as a UI key
   * and as the join key between current.json and factors.json.
   * Example: "economic_stress"
   */
  id: string;

  /** Human-readable display name shown in the UI. Example: "Economic Inequality" */
  name: string;

  /**
   * Normalized intensity of this factor. Range: 0.0–1.0 (inclusive).
   * 0.0 = minimal presence; 1.0 = maximum intensity.
   * NOT a percentage (0–100); NOT a raw data value.
   */
  value: number;

  /** Whether this factor is currently pushing the composite score up, down, or is neutral. */
  direction: FactorDirection;

  /**
   * Relative weight of this factor in the composite score calculation.
   * Range: 0.0–1.0. All factor weights in a current.json MUST sum to 1.0.
   */
  weight: number;
}

/**
 * current.json — the live snapshot displayed on the dashboard.
 * Updated by the pipeline whenever a new score is calculated (weekly in v1).
 */
export interface CurrentData {
  /**
   * Schema reference — not rendered in UI, used for debugging and pipeline validation.
   * Value must be "src/lib/data.ts#CurrentData".
   */
  _schema: string;

  /**
   * Composite revolution probability score.
   * Range: 0–100 (integer). 0 = no risk; 100 = maximum risk.
   */
  score: number;

  /**
   * ISO 8601 timestamp of when this score was calculated.
   * Must include timezone (Z or offset). Example: "2026-03-01T00:00:00Z"
   */
  timestamp: string;

  /** Human-readable zone label for the current score range. Derived from score thresholds. */
  zone: ZoneLabel;

  /**
   * Ordered list of contributing factors (highest weight first).
   * v1 UI is designed for 5–6 factors. Pipeline should respect this practical constraint.
   */
  factors: Factor[];

  /** Bootstrap confidence interval from ensemble scoring. */
  _bootstrap_ci?: {
    lower: number;
    upper: number;
    width: number;
    n: number;
  };
  /** List of model IDs that contributed to this score. */
  _models_run?: string[];
  /** Total number of models expected in the ensemble. */
  _models_expected?: number;
  /** Fraction of input variables with available data (0.0-1.0). */
  _data_coverage?: number;
  /** ISO 8601 timestamp of when the pipeline generated this file. */
  _generated_at?: string;
  /** Overall confidence assessment of the score. */
  _confidence?: 'high' | 'normal' | 'low' | 'degraded';
}

// ---------------------------------------------------------------------------
// history.json — HistoryData
// ---------------------------------------------------------------------------

/** A single point in the historical time series. */
export interface HistoryEntry {
  /**
   * ISO 8601 date string (date only, no time component).
   * Example: "2026-03-01"
   * Entries must be in ascending chronological order.
   */
  date: string;

  /** Composite score at that date. Range: 0–100 (integer). */
  score: number;
}

/**
 * history.json — the full weekly time series powering the trend chart.
 * Wrapped in an object (not a bare array) to allow future metadata additions
 * (e.g., last_updated, version) without a breaking schema change.
 * Minimum 12 entries required for the trend chart to render meaningfully.
 */
export interface HistoryData {
  /**
   * Schema reference — not rendered in UI.
   * Value must be "src/lib/data.ts#HistoryData".
   */
  _schema: string;

  /**
   * Chronologically ordered array of weekly score snapshots.
   * Must contain at least 12 entries. Entries must not be flat
   * (score variation of at least 10 points across the series).
   */
  entries: HistoryEntry[];
}

// ---------------------------------------------------------------------------
// factors.json — FactorsData
// ---------------------------------------------------------------------------

/** A single time-series point for a factor's historical data. */
export interface FactorHistoryEntry {
  /** ISO 8601 date string. Example: "2026-03-01" */
  date: string;

  /**
   * Normalized factor value at this date. Range: 0.0–1.0.
   * Same scale and meaning as Factor.value in current.json.
   */
  value: number;
}

/**
 * Detailed per-factor data including description and mini time series.
 * The id field is the join key to Factor.id in current.json.
 */
export interface FactorDetail {
  /**
   * Must match Factor.id in current.json exactly.
   * Pipeline uses this as the stable identifier across all three files.
   */
  id: string;

  /** Human-readable display name. Must match Factor.name in current.json. */
  name: string;

  /**
   * Explanation of what this factor measures and why it matters.
   * Displayed in expanded factor detail views (Phase 2+).
   * Should be 1–3 sentences; plain language, no jargon.
   */
  description: string;

  /**
   * Current normalized value. Range: 0.0–1.0.
   * Must match Factor.value for the same factor in current.json.
   */
  current_value: number;

  /**
   * Mini time series for this factor (for sparklines or drill-down charts).
   * 3 entries is sufficient for Phase 1 and Phase 2 sparklines.
   * Entries in ascending chronological order.
   */
  historical: FactorHistoryEntry[];
}

// ---------------------------------------------------------------------------
// benchmarks.json — BenchmarksData
// ---------------------------------------------------------------------------

/** A factor value with scholarly context note. */
export interface BenchmarkFactorValue {
  value: number;
  note: string;
}

/** Known factor IDs used in benchmark comparisons (5 domains from Phase 3). */
export type BenchmarkFactorId =
  | 'economic_stress'
  | 'political_polarization'
  | 'institutional_quality'
  | 'social_mobilization'
  | 'information_media';

/** A single historical revolution benchmark. */
export interface Benchmark {
  id: string;
  name: string;
  country: string;
  year: number;
  narrative: string;
  factors: Record<BenchmarkFactorId, BenchmarkFactorValue>;
  composite_estimate: number;
  keystat: string;
  sources: string[];
}

/** benchmarks.json — historical revolution benchmarks for comparison. */
export interface BenchmarksData {
  _schema: string;
  _note: string;
  benchmarks: Benchmark[];
}

/**
 * factors.json — detailed per-factor data for breakdown and drill-down views.
 * Contains the same factors as current.json but with descriptions and history.
 */
export interface FactorsData {
  /**
   * Schema reference — not rendered in UI.
   * Value must be "src/lib/data.ts#FactorsData".
   */
  _schema: string;

  /**
   * Array of detailed factor records.
   * Must contain an entry for every factor id that appears in current.json.
   */
  factors: FactorDetail[];
}

// ---------------------------------------------------------------------------
// factions.json — FactionsData
// ---------------------------------------------------------------------------

/** Demographics, geography, and institutional anchors for a faction. */
export interface FactionBase {
  demographics: string;
  geography: string;
  institutions: string;
}

/** Which Revolution Index factor a faction responds to. */
export interface FactionFactorAlignment {
  primary: BenchmarkFactorId;
  secondary: BenchmarkFactorId;
  description: string;
}

/** Faction stance toward revolution. */
export type FactionStance =
  | 'pro-revolution'
  | 'anti-revolution'
  | 'opportunistic'
  | 'conditional'
  | 'kingmaker';

/** A projected faction in a US instability scenario. */
export interface Faction {
  id: string;
  name: string;
  tagline: string;
  color: string;
  stance: FactionStance;
  stanceLabel: string;
  base: FactionBase;
  factorAlignment: FactionFactorAlignment;
  alliances: string[];
  conflicts: string[];
  wildcard: string;
}

/** factions.json — projected faction archetypes. */
export interface FactionsData {
  _schema: string;
  _note: string;
  factions: Faction[];
}

// ---------------------------------------------------------------------------
// policies.json — PoliciesData
// ---------------------------------------------------------------------------

/** A single policy recommendation with projected effect. */
export interface PolicyRecommendation {
  title: string;
  description: string;
  projectedEffect: string;
  precedent: string;
}

/** One side of the dual-perspective panel (stability or acceleration). */
export interface PolicyPanel {
  header: string;
  framing: string;
  policies: PolicyRecommendation[];
}

/** Policy analysis for a single Revolution Index factor. */
export interface FactorPolicies {
  id: BenchmarkFactorId;
  name: string;
  currentValue: number;
  weight: number;
  stability: PolicyPanel;
  acceleration: PolicyPanel;
}

/** policies.json — dual-perspective policy analysis by factor. */
export interface PoliciesData {
  _schema: string;
  _note: string;
  factors: FactorPolicies[];
}

// ---------------------------------------------------------------------------
// faction-profiles.json — FactionProfilesData
// ---------------------------------------------------------------------------

/** Convert faction ID (right_populists) to URL slug (right-populists). */
export function factionIdToSlug(id: string): string {
  return id.replace(/_/g, '-');
}

/** Convert URL slug (right-populists) back to faction ID (right_populists). */
export function factionSlugToId(slug: string): string {
  return slug.replace(/-/g, '_');
}

/** A single section in a faction's dossier profile. */
export interface FactionProfileSection {
  heading: string;
  paragraphs: string[];
}

/** Full dossier profile for a single faction. */
export interface FactionProfile {
  factionId: string;
  sections: FactionProfileSection[];
}

/** faction-profiles.json — deep-dive dossier content for all factions. */
export interface FactionProfilesData {
  _schema: string;
  _note: string;
  profiles: Record<string, FactionProfile>;
}
