export interface Trip {
  trip_id: string;
  driver_id: string;
  driver_car: string;
  capacity: number;
  destination: string;
  pickup_location: string;
  start_datetime: string;
  return_datetime: string;
  cost_per_passenger: number;
  passengers: string[];
}

export interface TripRequest {
  request_id: string;
  passenger_id: string;
  destination: string;
  earliest_start_date: string;
  latest_start_date: string;
  status: string;
  trip_id?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateTripBody {
  driver_id: string;
  driver_car: string;
  capacity: number;
  destination: string;
  pickup_location: string;
  start_datetime: string;
  return_datetime: string;
  cost_per_passenger: number;
}

export interface CreateTripRequestBody {
  passenger_id: string;
  destination: string;
  earliest_start_date: string;
  latest_start_date: string;
}

const API_URL = typeof window === 'undefined' 
  ? (process.env.INTERNAL_API_URL || 'http://trips-microservice:5001') 
  : (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001');

export async function getTrips(query?: { pickup?: string; destination?: string; date?: string }): Promise<Trip[]> {
  const params = new URLSearchParams();
  if (query?.pickup) params.append('pickup', query.pickup);
  if (query?.destination) params.append('destination', query.destination);
  if (query?.date) params.append('date', query.date);

  const res = await fetch(`${API_URL}/trips/?${params.toString()}`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch trips');
  return res.json();
}

export async function createTrip(trip: CreateTripBody): Promise<{ trip_id: string }> {
  const res = await fetch(`${API_URL}/trips/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(trip),
  });
  if (!res.ok) throw new Error('Failed to create trip');
  return res.json();
}

export async function getTripRequests(query?: { destination?: string }): Promise<TripRequest[]> {
  const params = new URLSearchParams();
  if (query?.destination) params.append('destination', query.destination);

  const res = await fetch(`${API_URL}/trips/requests?${params.toString()}`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch trip requests');
  return res.json();
}

export async function createTripRequest(request: CreateTripRequestBody): Promise<{ request_id: string }> {
  const res = await fetch(`${API_URL}/trips/requests`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  if (!res.ok) throw new Error('Failed to create trip request');
  return res.json();
}

export async function joinTrip(tripId: string, passengerId: string): Promise<void> {
  const res = await fetch(`${API_URL}/trips/${tripId}/join`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ passenger_id: passengerId }),
  });
  if (!res.ok) throw new Error('Failed to join trip');
}
