import { getTripRequests } from "@/lib/api";
import { Calendar, User } from "lucide-react";
import CreateRequestButton from "@/components/CreateRequestButton";
import Search from "@/components/Search";

export default async function RequestsPage({
  searchParams,
}: {
  searchParams?: {
    query?: string;
  };
}) {
  const query = searchParams?.query || "";
  const requests = await getTripRequests({ destination: query });

  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-text">Trip Requests</h1>
          <p className="text-text-muted">Manage and view all trip requests.</p>
        </div>
        <CreateRequestButton />
      </div>

      <Search placeholder="Search requests by destination..." />

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
