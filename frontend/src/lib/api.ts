import type { VideoBrief, VideoCreationResponse, VideoListItem } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

// Reasoning: ek helper function jo error-handling har jagah repeat na karni pare —
// bilkul jaisay humne Python mein AssetBase banaya tha duplicate fields ke liye
async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => null);
    throw new Error(errorBody?.detail ?? `Request failed: ${response.status}`);
  }

  return response.json();
}

export function createVideo(brief: VideoBrief): Promise<VideoCreationResponse> {
  return apiFetch<VideoCreationResponse>("/create-video", {
    method: "POST",
    body: JSON.stringify(brief),
  });
}

export function listVideos(): Promise<VideoListItem[]> {
  return apiFetch<VideoListItem[]>("/videos");
}

export function getVideo(videoId: string) {
  return apiFetch(`/videos/${videoId}`);
}
