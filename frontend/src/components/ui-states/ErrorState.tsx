import Link from "next/link";
import { Button } from "@/components/ui/button";

export function ErrorState({
  message,
  backHref = "/create",
  backLabel = "Start Over",
}: {
  message: string;
  backHref?: string;
  backLabel?: string;
}) {
  return (
    <main className="max-w-2xl mx-auto p-6 text-center">
      <p className="mb-4 text-red-600">{message}</p>
      <Link href={backHref}>
        <Button variant="outline">{backLabel}</Button>
      </Link>
    </main>
  );
}