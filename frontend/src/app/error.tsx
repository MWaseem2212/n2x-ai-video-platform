"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/button";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <main className="max-w-2xl mx-auto p-6 text-center">
      <h2 className="text-xl font-semibold mb-2 text-red-600">Something went wrong</h2>
      <p className="mb-4 text-muted-foreground">{error.message}</p>
      <Button onClick={() => reset()}>Try Again</Button>
    </main>
  );
}