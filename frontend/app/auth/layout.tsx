"use client";

import { ReactNode } from "react";
import { ThemeToggle } from "@/components/ui/theme-toggle";

export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50 dark:from-[#0d0d11] dark:via-[#111216] dark:to-[#1a1b20] transition-colors duration-200">
      <div className="absolute top-6 right-6 z-10">
        <ThemeToggle />
      </div>
      <div className="mx-auto flex max-w-5xl flex-col items-center justify-center px-6 md:px-12 lg:px-24 py-16">
        {children}
      </div>
    </div>
  );
}
