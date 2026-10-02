"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import type { VideoCreationResponse } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function ResultsPage() {
  const [result, setResult] = useState<VideoCreationResponse | null>(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const stored = sessionStorage.getItem("latest_video_result");
    if (stored) {
      setResult(JSON.parse(stored));
    }
    setLoaded(true);
  }, []);

  if (!loaded) return null;

  if (!result) {
    return (
      <main className="max-w-xl mx-auto p-6 text-center">
        <p className="mb-4">No video result found.</p>
        <Link href="/create">
          <Button>Create a Video</Button>
        </Link>
      </main>
    );
  }

  const { video_plan, reuse_result, provider_decision, cost_estimate } = result;

  return (
    <main className="max-w-2xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold" style={{ color: "var(--n2x-navy)" }}>
        {video_plan.title}
      </h1>

      <Card>
        <CardHeader>
          <CardTitle>Proposed Structure</CardTitle>
        </CardHeader>
        <CardContent>
          <ol className="list-decimal list-inside space-y-1">
            {video_plan.proposed_structure.map((scene, i) => (
              <li key={i}>{scene}</li>
            ))}
          </ol>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Reuse Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="mb-2 font-semibold" style={{ color: "var(--n2x-teal)" }}>
            {reuse_result.reuse_score}% Existing Assets Reusable
          </p>
          <ul className="text-sm space-y-1">
            <li>Avatar: {reuse_result.breakdown.avatar.asset_name ?? "New generation required"}</li>
            <li>Voice: {reuse_result.breakdown.voice.asset_name ?? "New generation required"}</li>
            <li>Background: {reuse_result.breakdown.background.asset_name ?? "New generation required"}</li>
          </ul>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Provider & Cost</CardTitle>
        </CardHeader>
        <CardContent>
          <p>Recommended Provider: <strong>{provider_decision.recommended}</strong></p>
          <p>Estimated Total: <strong>£{cost_estimate.estimated_total}</strong></p>
          <p>
            RAG Saving: £{cost_estimate.rag_saving_amount} ({cost_estimate.rag_saving_percentage}%)
          </p>
        </CardContent>
      </Card>

      <Link href="/library">
        <Button variant="outline">View Video Library</Button>
      </Link>
    </main>
  );
}