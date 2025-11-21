import { getTripRequests } from "@/lib/api";
import { Search, Calendar, User } from "lucide-react";
import CreateRequestButton from "@/components/CreateRequestButton";

export default async function RequestsPage() {
  const requests = await getTripRequests();

  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-text">Trip Requests</h1>
          <p className="text-text-muted">Manage and view all trip requests.</p>
        </div>
        <CreateRequestButton />
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-text-muted" />
        <input
          type="text"
          placeholder="Search requests..."
          className="w-full rounded-lg border border-surface-highlight bg-surface py-2 pl-10 pr-4 text-sm text-text placeholder:text-text-muted focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
        />
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {requests.length === 0 ? (
          <div className="col-span-full rounded-xl border border-surface-highlight bg-surface p-8 text-center">
            <p className="text-text-muted">No requests found. Create one to get started.</p>
          </div>
        ) : (
          requests.map((req) => (
            <div key={req.request_id} className="flex flex-col gap-4 rounded-xl border border-surface-highlight bg-surface p-6 transition-colors hover:border-primary/50">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-semibold text-text">{req.destination}</h3>
                  <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                    req.status === 'pending' ? 'bg-yellow-500/10 text-yellow-500' : 
                    req.status === 'accepted' ? 'bg-primary/10 text-primary' : 
                    'bg-red-500/10 text-red-500'
                  }`}>
                    {req.status}
                  </span>
                </div>
              </div>
              
              <div className="flex flex-col gap-2 text-sm text-text-muted">
                <div className="flex items-center gap-2">
                  <Calendar size={14} />
                  <span>{new Date(req.earliest_start_date).toLocaleDateString()} - {new Date(req.latest_start_date).toLocaleDateString()}</span>
                </div>
                <div className="flex items-center gap-2">
                  <User size={14} />
                  <span>{req.passenger_id}</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
