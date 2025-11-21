import { getTrips } from "@/lib/api";
import { Search, Calendar, User } from "lucide-react";
import CreateTripButton from "@/components/CreateTripButton";

export default async function TripsPage() {
  const trips = await getTrips();

  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-text">Trips</h1>
          <p className="text-text-muted">Manage and view all available trips.</p>
        </div>
        <CreateTripButton />
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-text-muted" />
        <input
          type="text"
          placeholder="Search trips..."
          className="w-full rounded-lg border border-surface-highlight bg-surface py-2 pl-10 pr-4 text-sm text-text placeholder:text-text-muted focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
        />
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {trips.length === 0 ? (
          <div className="col-span-full rounded-xl border border-surface-highlight bg-surface p-8 text-center">
            <p className="text-text-muted">No trips found. Create one to get started.</p>
          </div>
        ) : (
          trips.map((trip) => (
            <div key={trip.trip_id} className="flex flex-col gap-4 rounded-xl border border-surface-highlight bg-surface p-6 transition-colors hover:border-primary/50">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-semibold text-text">{trip.destination}</h3>
                  <p className="text-sm text-text-muted">from {trip.pickup_location}</p>
                </div>
                <span className="rounded-full bg-primary/10 px-2.5 py-0.5 text-xs font-medium text-primary">
                  ${trip.cost_per_passenger}
                </span>
              </div>
              
              <div className="flex flex-col gap-2 text-sm text-text-muted">
                <div className="flex items-center gap-2">
                  <Calendar size={14} />
                  <span>{new Date(trip.start_datetime).toLocaleDateString()}</span>
                </div>
                <div className="flex items-center gap-2">
                  <User size={14} />
                  <span>{trip.driver_id} • {trip.passengers.length}/{trip.capacity} seats</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
