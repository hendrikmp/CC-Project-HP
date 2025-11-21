"use client";

import { useState } from "react";
import { UserPlus, X } from "lucide-react";
import { joinTrip } from "@/lib/api";
import { useRouter } from "next/navigation";

interface JoinTripButtonProps {
  tripId: string;
  currentPassengers: number;
  capacity: number;
}

export default function JoinTripButton({ tripId, currentPassengers, capacity }: JoinTripButtonProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [passengerId, setPassengerId] = useState("");
  const router = useRouter();

  const isFull = currentPassengers >= capacity;

  const handleJoin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await joinTrip(tripId, passengerId);
      setIsOpen(false);
      setPassengerId("");
      router.refresh();
    } catch (error) {
      console.error("Failed to join trip:", error);
      alert("Failed to join trip. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  if (isFull) {
    return (
      <button disabled className="flex items-center gap-2 rounded-lg bg-surface-highlight px-3 py-1.5 text-xs font-medium text-text-muted opacity-50 cursor-not-allowed">
        Full
      </button>
    );
  }

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="flex items-center gap-2 rounded-lg bg-primary/10 px-3 py-1.5 text-xs font-medium text-primary transition-colors hover:bg-primary/20"
      >
        <UserPlus size={14} />
        Join
      </button>

      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
          <div className="w-full max-w-sm rounded-xl border border-surface-highlight bg-surface p-6 shadow-xl">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-lg font-bold text-text">Join Trip</h2>
              <button
                onClick={() => setIsOpen(false)}
                className="rounded-lg p-2 text-text-muted hover:bg-surface-highlight hover:text-text"
              >
                <X size={20} />
              </button>
            </div>

            <p className="mb-4 text-sm text-text-muted">
              Are you sure you want to join this trip? Please enter your Passenger ID to confirm.
            </p>

            <form onSubmit={handleJoin} className="flex flex-col gap-4">
              <div className="flex flex-col gap-2">
                <label className="text-sm font-medium text-text-muted">Passenger ID</label>
                <input
                  required
                  value={passengerId}
                  onChange={(e) => setPassengerId(e.target.value)}
                  className="rounded-lg border border-surface-highlight bg-background px-3 py-2 text-sm text-text focus:border-primary focus:outline-none"
                  placeholder="e.g. john_doe"
                />
              </div>

              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => setIsOpen(false)}
                  className="flex-1 rounded-lg border border-surface-highlight bg-transparent px-4 py-2 text-sm font-semibold text-text hover:bg-surface-highlight"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="flex-1 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-background hover:bg-primary-dark disabled:opacity-50"
                >
                  {isLoading ? "Joining..." : "Confirm Join"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
