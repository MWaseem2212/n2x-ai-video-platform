export function LoadingState({ message = "Loading..." }: { message?: string }) {
  return (
    <main className="max-w-2xl mx-auto p-6 text-center text-muted-foreground">
      {message}
    </main>
  );
}