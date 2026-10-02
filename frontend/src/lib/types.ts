// Reasoning: Ye types humare Python VideoBrief, VideoPlan, aur API response
// models se exactly match karte hain — Step 1 aur Step 10 (backend) se

export type Sector =
  | "adult_care"
  | "early_years"
  | "fostering"
  | "childrens_homes"
  | "education"
  | "childrens_social_work"
  | "adult_social_work"
  | "leaving_care"
  | "other";

export interface VideoBrief {
  sector: Sector;
  country: string;
  audience: string;
  tone: string;
  culture?: string;
  video_type: string;
  video_format: string;
  duration_seconds: number;
  description: string;
}

export interface VideoPlan {
  title: string;
  proposed_structure: string[];
  estimated_total_duration: number;
}

export interface ReuseBreakdownItem {
  status: string;
  score: number;
  asset_name: string | null;
}

export interface ReuseResult {
  reuse_score: number;
  new_generation_required: number;
  breakdown: {
    avatar: ReuseBreakdownItem;
    voice: ReuseBreakdownItem;
    background: ReuseBreakdownItem;
  };
}

export interface ProviderDecision {
  recommended: string | null;
  cost?: number;
  all_scores: {
    provider: string;
    has_avatar: boolean;
    cost: number;
  }[];
  fallback_log?: { provider: string; status: string; reason: string }[];
}

export interface CostEstimate {
  provider: string;
  estimated_total: number;
  estimated_cost_without_reuse: number;
  rag_saving_amount: number;
  rag_saving_percentage: number;
}

export interface VideoCreationResponse {
  video_id: string;
  video_plan: VideoPlan;
  reuse_result: ReuseResult;
  provider_decision: ProviderDecision;
  cost_estimate: CostEstimate;
}

export interface VideoListItem {
  id: string;
  title: string;
  sector: string;
  provider: string;
  status: string;
  duration_seconds: number;
  created_at: string;
}
