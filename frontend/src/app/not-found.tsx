import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function NotFound() {
  return (
    <main className="max-w-2xl mx-auto p-6 text-center">
      <h2 className="text-xl font-semibold mb-2">Page Not Found</h2>
      <p className="mb-4 text-muted-foreground">
        The page you&apos;re looking for doesn&apos;t exist.
      </p>
      <Link href="/create">
        <Button>Go to Create Video</Button>
      </Link>
    </main>
  );
}