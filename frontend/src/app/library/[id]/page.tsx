"use client";

import { useEffect, useState, use } from "react";
import Link from "next/link";
import { getVideo } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { LoadingState } from "@/components/ui-states/LoadingState";
import { ErrorState } from "@/components/ui-states/ErrorState";

interface VideoDetail {
  id: string;
  title: string;
  sector: string;
  country: string;
  avatar_name: string | null;
  provider: string;
  status: string;
  duration_seconds: number;
  created_at: string;
}

export default function VideoDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  // Reasoning: Next.js 15+ mein 'params' ab ek Promise hai (pehle plain object
  // hota tha) — React ka 'use()' hook isay unwrap karta hai
  const { id } = use(params);

  const [video, setVideo] = useState<VideoDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getVideo(id)
      .then((data) => setVideo(data as VideoDetail))
      .catch((err) => setError(err instanceof Error ? err.message : "Video not found"))
      .finally(() => setIsLoading(false));
  }, [id]);

  if (isLoading) {
  return <LoadingState message="Loading video details..." />;
}

if (error || !video) {
  return <ErrorState message={error ?? "Video not found"} backHref="/library" backLabel="Back to Library" />;
}

  return (
    <main className="max-w-2xl mx-auto p-6 space-y-4">
      <Link href="/library" className="text-sm underline" style={{ color: "var(--n2x-teal)" }}>
        ← Back to Library
      </Link>

      <h1 className="text-2xl font-bold" style={{ color: "var(--n2x-navy)" }}>
        {video.title}
      </h1>

      <Card>
        <CardHeader>
          <CardTitle>Details</CardTitle>
        </CardHeader>
        <CardContent className="space-y-1 text-sm">
          <p>Sector: {video.sector}</p>
          <p>Country: {video.country}</p>
          <p>Avatar: {video.avatar_name ?? "N/A"}</p>
          <p>Provider: {video.provider}</p>
          <p>Duration: {video.duration_seconds} seconds</p>
          <p>
            Status: <span style={{ color: "var(--n2x-teal)" }}>{video.status}</span>
          </p>
          <p>Created: {new Date(video.created_at).toLocaleString()}</p>
        </CardContent>
      </Card>
    </main>
  );
}