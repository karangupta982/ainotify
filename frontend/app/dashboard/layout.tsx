"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ReactNode } from "react";
import {
  LayoutGrid,
  UserRound,
  ListVideo,
  CreditCard,
  LogOut,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { ThemeToggle } from "@/components/ui/theme-toggle";

const navItems = [
  { href: "/dashboard", label: "Overview", icon: LayoutGrid },
  { href: "/dashboard/profile", label: "Profile", icon: UserRound },
  { href: "/dashboard/channels", label: "Channels", icon: ListVideo },
  { href: "/dashboard/billing", label: "Billing", icon: CreditCard },
];

export default function DashboardLayout({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const BASE_URL = process.env.NEXT_PUBLIC_BASE_URL;

  const signOut = async () => {
    try {
      const res = await fetch(`${BASE_URL}/api/auth/logout`, {
        method: "POST",
        credentials: "include",
      });
      if (res.ok) {
        window.location.href = "/auth/login";
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="min-h-screen bg-white dark:bg-[#0d0d11] transition-colors duration-200">
      <div className="mx-auto flex max-w-7xl gap-6 px-6 md:px-12 lg:px-24 py-8">
        {/* Sidebar Navigation */}
        <aside className="hidden w-64 shrink-0 flex-col gap-2 sm:flex">
          <Card padding="md" className="mb-4">
            <div className="flex items-center justify-between">
              <div className="text-sm font-semibold text-indigo-700 dark:text-indigo-400">
                AI Notify
              </div>
              <ThemeToggle />
            </div>
          </Card>
          <nav className="flex flex-col gap-1" aria-label="Main navigation">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors duration-200 cursor-pointer ${
                    isActive
                      ? "bg-indigo-50 dark:bg-[#1a1b20] text-indigo-700 dark:text-indigo-400"
                      : "text-slate-700 dark:text-gray-300 hover:bg-slate-100 dark:hover:bg-[#1a1b20]"
                  }`}
                  aria-current={isActive ? "page" : undefined}
                >
                  <Icon className="h-4 w-4" aria-hidden="true" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>
          <div className="mt-auto pt-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={signOut}
              className="w-full justify-start text-rose-600 dark:text-rose-400 hover:text-rose-700 dark:hover:text-rose-300 hover:bg-rose-50 dark:hover:bg-rose-950/20"
              leftIcon={<LogOut className="h-4 w-4" />}
              aria-label="Sign out of your account"
            >
              Sign out
            </Button>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 min-w-0 animate-fade-in">
          <div className="space-y-6">{children}</div>
        </main>
      </div>
    </div>
  );
}
