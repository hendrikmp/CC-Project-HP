"use client";

import { useState } from "react";
import { Plus, X } from "lucide-react";
import { createTripRequest, CreateTripRequestBody } from "@/lib/api";
import { useRouter } from "next/navigation";

export default function CreateRequestButton() {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const [formData, setFormData] = useState<CreateTripRequestBody>({
    passenger_id: "",
    destination: "",
    earliest_start_date: "",
    latest_start_date: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await createTripRequest(formData);
      setIsOpen(false);
      router.refresh();
      // Reset form
      setFormData({
        passenger_id: "",
        destination: "",
        earliest_start_date: "",
        latest_start_date: "",
      });
    } catch (error) {
      console.error("Failed to create request:", error);
      alert("Failed to create request. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-background transition-transform hover:scale-105 active:scale-95"
      >
        <Plus size={16} />
        New Request
      </button>

      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
          <div className="w-full max-w-md rounded-xl border border-surface-highlight bg-surface p-6 shadow-xl">
            <div className="mb-6 flex items-center justify-between">
              <h2 className="text-xl font-bold text-text">Create Trip Request</h2>
              <button
                onClick={() => setIsOpen(false)}
                className="rounded-lg p-2 text-text-muted hover:bg-surface-highlight hover:text-text"
              >
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
              <div className="flex flex-col gap-2">
                <label className="text-sm font-medium text-text-muted">Passenger ID</label>
                <input
                  required
                  name="passenger_id"
                  value={formData.passenger_id}
                  onChange={handleChange}
                  className="rounded-lg border border-surface-highlight bg-background px-3 py-2 text-sm text-text focus:border-primary focus:outline-none"
                  placeholder="e.g. jane_doe"
                />
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-sm font-medium text-text-muted">Destination</label>
                <input
                  required
                  name="destination"
                  value={formData.destination}
                  onChange={handleChange}
                  className="rounded-lg border border-surface-highlight bg-background px-3 py-2 text-sm text-text focus:border-primary focus:outline-none"
                  placeholder="City or Address"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-medium text-text-muted">Earliest Date</label>
                  <input
                    required
                    type="datetime-local"
                    name="earliest_start_date"
                    value={formData.earliest_start_date}
                    onChange={handleChange}
                    className="rounded-lg border border-surface-highlight bg-background px-3 py-2 text-sm text-text focus:border-primary focus:outline-none"
                  />
                </div>
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-medium text-text-muted">Latest Date</label>
                  <input
                    required
                    type="datetime-local"
                    name="latest_start_date"
                    value={formData.latest_start_date}
                    onChange={handleChange}
                    className="rounded-lg border border-surface-highlight bg-background px-3 py-2 text-sm text-text focus:border-primary focus:outline-none"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="mt-4 rounded-lg bg-primary px-4 py-2 font-semibold text-background transition-transform hover:scale-105 active:scale-95 disabled:opacity-50"
              >
                {isLoading ? "Creating..." : "Create Request"}
              </button>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
