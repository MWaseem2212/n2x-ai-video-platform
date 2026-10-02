"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { listVideos } from "@/lib/api";
import type { VideoListItem } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { LoadingState } from "@/components/ui-states/LoadingState";
import { ErrorState } from "@/components/ui-states/ErrorState";

function countBy(videos: VideoListItem[], key: keyof VideoListItem) {
  const counts: Record<string, number> = {};
  for (const video of videos) {
    const value = String(video[key]);
    counts[value] = (counts[value] ?? 0) + 1;
  }
  return counts;
}

export default function HomePage() {
  const [videos, setVideos] = useState<VideoListItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listVideos()
      .then(setVideos)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load dashboard"))
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading) return <LoadingState message="Loading dashboard..." />;
  if (error) return <ErrorState message={error} backHref="/create" backLabel="Create a Video" />;

  const statusCounts = countBy(videos, "status");
  const providerCounts = countBy(videos, "provider");
  const recentVideos = [...videos]
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 5);

  return (
    <main className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold" style={{ color: "var(--n2x-navy)" }}>
          N2X Dashboard
        </h1>
        <Link href="/create">
          <Button>+ Create Video</Button>
        </Link>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-sm text-muted-foreground">Total Videos</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold" style={{ color: "var(--n2x-teal)" }}>
              {videos.length}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm text-muted-foreground">By Status</CardTitle>
          </CardHeader>
          <CardContent className="text-sm space-y-1">
            {Object.entries(statusCounts).map(([status, count]) => (
              <p key={status}>
                {status}: <strong>{count}</strong>
              </p>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm text-muted-foreground">By Provider</CardTitle>
          </CardHeader>
          <CardContent className="text-sm space-y-1">
            {Object.entries(providerCounts).map(([provider, count]) => (
              <p key={provider}>
                {provider}: <strong>{count}</strong>
              </p>
            ))}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Videos</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          {recentVideos.length === 0 && (
            <p className="text-muted-foreground text-sm">No videos created yet.</p>
          )}
          {recentVideos.map((video) => (
            <Link
              key={video.id}
              href={`/library/${video.id}`}
              className="block text-sm underline"
              style={{ color: "var(--n2x-teal)" }}
            >
              {video.title} — {video.sector}
            </Link>
          ))}
        </CardContent>
      </Card>

      <Link href="/library">
        <Button variant="outline">View Full Library</Button>
      </Link>
    </main>
  );
}