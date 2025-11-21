"use client";

import { useState } from "react";
import { Plus, X } from "lucide-react";
import { createTrip, CreateTripBody } from "@/lib/api";
import { useRouter } from "next/navigation";

export default function CreateTripButton() {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const [formData, setFormData] = useState<CreateTripBody>({
    driver_id: "",
    driver_car: "",
    capacity: 4,
    destination: "",
    pickup_location: "",
    start_datetime: "",
    return_datetime: "",
    cost_per_passenger: 0,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await createTrip(formData);
      setIsOpen(false);
      router.refresh();
      // Reset form
      setFormData({
        driver_id: "",
        driver_car: "",
        capacity: 4,
        destination: "",
        pickup_location: "",
        start_datetime: "",
        return_datetime: "",
        cost_per_passenger: 0,
      });
    } catch (error) {
      console.error("Failed to create trip:", error);
      alert("Failed to create trip. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === "capacity" || name === "cost_per_passenger" ? Number(value) : value,
    }));
  };

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-background transition-transform hover:scale-105 active:scale-95"
      >
        <Plus size={16} />
        New Trip
      </button>

      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
          <div className="w-full max-w-md rounded-xl border border-surface-highlight bg-surface p-6 shadow-xl">
            <div className="mb-6 flex items-center justify-between">
              <h2 className="text-xl font-bold text-text">Create New Trip</h2>
              <button
                onClick={() => setIsOpen(false)}
                className="rounded-lg p-2 text-text-muted hover:bg-surface-highlight hover:text-text"
              >
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-medium text-text-muted">Driver ID</label>
                  <input
                    required
                    name="driver_id"
                    value={formData.driver_id}
                    onChange={handleChange}
                    className="rounded-lg border border-surface-highlight bg-background px-3 py-2 text-sm text-text focus:border-primary focus:outline-none"
                    placeholder="e.g. john_doe"
                  />
                </div>
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-medium text-text-muted">Car Model</label>
                  <input
                    required
                    name="driver_car"
                    value={formData.driver_car}
                    onChange={handleChange}
                    className="rounded-lg border border-surface-highlight bg-background px-3 py-2 text-sm text-text focus:border-primary focus:outline-none"
                    placeholder="e.g. Tesla Model 3"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-medium text-text-muted">Pickup</label>
                  <input
                    required
                    name="pickup_location"
                    value={formData.pickup_location}
                    onChange={handleChange}
                    className="rounded-lg border border-surface-highlight bg-background px-3 py-2 text-sm text-text focus:border-primary focus:outline-none"
                    placeholder="City or Address"
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
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-medium text-text-muted">Start Time</label>
                  <input
                    required
                    type="datetime-local"
                    name="start_datetime"
                    value={formData.start_datetime}
                    onChange={handleChange}
                    className="rounded-lg border border-surface-highlight bg-background px-3 py-2 text-sm text-text focus:border-primary focus:outline-none"
                  />
                </div>
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-medium text-text-muted">Return Time</label>
                  <input
                    required
                    type="datetime-local"
                    name="return_datetime"
                    value={formData.return_datetime}
                    onChange={handleChange}
                    className="rounded-lg border border-surface-highlight bg-background px-3 py-2 text-sm text-text focus:border-primary focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-medium text-text-muted">Capacity</label>
                  <input
                    required
                    type="number"
                    min="1"
                    name="capacity"
                    value={formData.capacity}
                    onChange={handleChange}
                    className="rounded-lg border border-surface-highlight bg-background px-3 py-2 text-sm text-text focus:border-primary focus:outline-none"
                  />
                </div>
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-medium text-text-muted">Cost ($)</label>
                  <input
                    required
                    type="number"
                    min="0"
                    step="0.01"
                    name="cost_per_passenger"
                    value={formData.cost_per_passenger}
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
                {isLoading ? "Creating..." : "Create Trip"}
              </button>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
