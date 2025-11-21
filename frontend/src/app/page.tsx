import { getTrips, getTripRequests } from "@/lib/api";
import { ArrowRight, Plus } from "lucide-react";
import Link from "next/link";

export default async function Home() {
  const [trips, requests] = await Promise.all([getTrips(), getTripRequests()]);
  
  const activeTrips = trips.length;
  const pendingRequests = requests.filter(r => r.status === 'pending').length;
  const totalPassengers = trips.reduce((acc, trip) => acc + trip.passengers.length, 0);

  return (
    <div className="flex flex-col gap-8">
      <div className="flex flex-col gap-2">
        <h1 className="text-4xl font-bold tracking-tight text-text">Dashboard</h1>
        <p className="text-text-muted">Welcome back to BlaBlaTrip.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-xl border border-surface-highlight bg-surface p-6 shadow-sm transition-all hover:shadow-md">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-text-muted">Active Trips</h3>
          </div>
          <div className="mt-4 text-3xl font-bold text-text">{activeTrips}</div>
        </div>
        <div className="rounded-xl border border-surface-highlight bg-surface p-6 shadow-sm transition-all hover:shadow-md">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-text-muted">Pending Requests</h3>
          </div>
          <div className="mt-4 text-3xl font-bold text-text">{pendingRequests}</div>
        </div>
        <div className="rounded-xl border border-surface-highlight bg-surface p-6 shadow-sm transition-all hover:shadow-md">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-text-muted">Total Passengers</h3>
          </div>
          <div className="mt-4 text-3xl font-bold text-text">{totalPassengers}</div>
        </div>
      </div>

      <div className="flex gap-4">
        <Link
          href="/trips"
          className="flex items-center gap-2 rounded-lg bg-primary px-6 py-3 text-sm font-semibold text-background transition-transform hover:scale-105 active:scale-95"
        >
          <Plus size={18} />
          Create Trip
        </Link>
        <Link
          href="/requests"
          className="flex items-center gap-2 rounded-lg border border-surface-highlight bg-surface px-6 py-3 text-sm font-semibold text-text transition-colors hover:bg-surface-highlight"
        >
          View Requests
          <ArrowRight size={18} />
        </Link>
      </div>
    </div>
  );
}
