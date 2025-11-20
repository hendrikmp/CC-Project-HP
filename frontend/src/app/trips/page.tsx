import { Plus, Search } from "lucide-react";

export default function TripsPage() {
  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-text">Trips</h1>
          <p className="text-text-muted">Manage and view all available trips.</p>
        </div>
        <button className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-background transition-transform hover:scale-105 active:scale-95">
          <Plus size={16} />
          New Trip
        </button>
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-text-muted" />
        <input
          type="text"
          placeholder="Search trips..."
          className="w-full rounded-lg border border-surface-highlight bg-surface py-2 pl-10 pr-4 text-sm text-text placeholder:text-text-muted focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
        />
      </div>

      <div className="rounded-xl border border-surface-highlight bg-surface p-8 text-center">
        <p className="text-text-muted">No trips found. Create one to get started.</p>
      </div>
    </div>
  );
}
