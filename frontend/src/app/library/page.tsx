"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { listVideos } from "@/lib/api";
import type { VideoListItem } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LoadingState } from "@/components/ui-states/LoadingState";
import { ErrorState } from "@/components/ui-states/ErrorState";

export default function LibraryPage() {
  const [videos, setVideos] = useState<VideoListItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listVideos()
      .then(setVideos)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load videos"))
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading) {
  return <LoadingState message="Loading video library..." />;
}

if (error) {
  return <ErrorState message={error} backHref="/create" backLabel="Create a Video" />;
}

  if (videos.length === 0) {
    return (
      <main className="max-w-4xl mx-auto p-6 text-center">
        <p className="mb-4">No videos created yet.</p>
        <Link href="/create" className="underline" style={{ color: "var(--n2x-teal)" }}>
          Create your first video
        </Link>
      </main>
    );
  }

  return (
    <main className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6" style={{ color: "var(--n2x-navy)" }}>
        Video Library
      </h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {videos.map((video) => (
          <Link key={video.id} href={`/library/${video.id}`}>
            <Card className="hover:shadow-md transition-shadow cursor-pointer">
              <CardHeader>
                <CardTitle className="text-base">{video.title}</CardTitle>
              </CardHeader>
              <CardContent className="text-sm space-y-1">
                <p>Sector: {video.sector}</p>
                <p>Provider: {video.provider}</p>
                <p>Duration: {video.duration_seconds}s</p>
                <p style={{ color: "var(--n2x-teal)" }}>{video.status}</p>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </main>
  );
}