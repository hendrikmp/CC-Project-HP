"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Car, MapPin, Search } from "lucide-react";
import { motion } from "framer-motion";
import clsx from "clsx";

const navItems = [
  { name: "Dashboard", href: "/", icon: Car },
  { name: "Trips", href: "/trips", icon: MapPin },
  { name: "Requests", href: "/requests", icon: Search },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-surface-highlight bg-background/80 backdrop-blur-md">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/20 text-primary">
            <Car size={20} />
          </div>
          <span className="text-lg font-bold tracking-tight text-text">BlaBlaTrip</span>
        </div>

        <div className="flex items-center gap-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={clsx(
                  "relative flex items-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition-colors",
                  isActive
                    ? "text-primary"
                    : "text-text-muted hover:bg-surface hover:text-text"
                )}
              >
                {isActive && (
                  <motion.div
                    layoutId="navbar-indicator"
                    className="absolute inset-0 rounded-md bg-surface-highlight"
                    initial={false}
                    transition={{ type: "spring", stiffness: 500, damping: 30 }}
                  />
                )}
                <span className="relative z-10 flex items-center gap-2">
                  <item.icon size={16} />
                  {item.name}
                </span>
              </Link>
            );
          })}
        </div>

        <div className="flex items-center gap-4">
          <div className="h-8 w-8 rounded-full bg-surface-highlight" />
        </div>
      </div>
    </nav>
  );
}
