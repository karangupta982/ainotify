"use client";

import { Card } from "@/components/ui/card";
import { Section } from "@/components/ui/section";

export function Showcase() {
  return (
    <Section
      title="See it in action"
      description="Experience the power of personalized AI news curation. Every digest is tailored to your interests and expertise level."
      spacing="lg"
      className="py-24 relative overflow-hidden"
    >
      {/* Background elements */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 h-[600px] w-[600px] rounded-full bg-indigo-500/10 dark:bg-indigo-500/5 blur-3xl" />
        <div className="absolute right-0 top-0 h-96 w-96 rounded-full bg-purple-500/10 dark:bg-purple-500/5 blur-3xl" />
      </div>

      <div className="mx-auto max-w-5xl">

        {/* Large Preview Card */}
        <Card
          padding="none"
          className="relative overflow-hidden shadow-2xl dark:shadow-[0_0_60px_rgba(99,102,241,0.15)] border-2 border-slate-200 dark:border-[#2a2b31]"
        >
          {/* Email Digest Preview */}
          <div className="bg-gradient-to-br from-indigo-50 via-white to-purple-50 dark:from-indigo-950/30 dark:via-[#111216] dark:to-purple-950/30 p-8 md:p-12">
            {/* Email Header */}
            <div className="mb-8 space-y-4">
              <div className="flex items-center gap-4">
                <div className="h-12 w-12 rounded-full bg-gradient-to-br from-indigo-600 to-purple-600 dark:from-indigo-500 dark:to-purple-500 flex items-center justify-center">
                  <span className="text-white text-lg font-semibold">AI</span>
                </div>
                <div>
                  <div className="h-4 w-32 rounded bg-slate-300 dark:bg-slate-700 mb-2" />
                  <div className="h-3 w-24 rounded bg-slate-200 dark:bg-slate-800" />
                </div>
              </div>
              <div className="h-6 w-48 rounded bg-slate-200 dark:bg-slate-800" />
            </div>

            {/* Digest Content */}
            <div className="space-y-6">
              {/* Featured Article */}
              <div className="rounded-xl border border-slate-200 dark:border-[#2a2b31] bg-white dark:bg-[#1a1b20] p-6 shadow-lg">
                <div className="flex items-start gap-4">
                  <div className="h-20 w-20 rounded-lg bg-gradient-to-br from-indigo-100 to-purple-100 dark:from-indigo-900/30 dark:to-purple-900/30 flex-shrink-0" />
                  <div className="flex-1 space-y-3">
                    <div className="h-5 w-3/4 rounded bg-slate-300 dark:bg-slate-700" />
                    <div className="h-3 w-full rounded bg-slate-200 dark:bg-slate-800" />
                    <div className="h-3 w-5/6 rounded bg-slate-200 dark:bg-slate-800" />
                    <div className="flex items-center gap-2 pt-2">
                      <div className="h-2 w-2 rounded-full bg-indigo-500" />
                      <div className="h-3 w-20 rounded bg-slate-200 dark:bg-slate-800" />
                    </div>
                  </div>
                </div>
              </div>

              {/* Article Grid */}
              <div className="grid gap-4 md:grid-cols-2">
                {[1, 2, 3, 4].map((i) => (
                  <div
                    key={i}
                    className="rounded-lg border border-slate-200 dark:border-[#2a2b31] bg-white dark:bg-[#1a1b20] p-4"
                  >
                    <div className="h-16 w-full rounded bg-slate-200 dark:bg-slate-800 mb-3" />
                    <div className="h-3 w-full rounded bg-slate-200 dark:bg-slate-800 mb-2" />
                    <div className="h-3 w-3/4 rounded bg-slate-200 dark:bg-slate-800" />
                  </div>
                ))}
              </div>

              {/* Summary Section */}
              <div className="rounded-xl bg-indigo-50 dark:bg-indigo-950/30 p-6 border border-indigo-100 dark:border-indigo-900/50">
                <div className="h-4 w-32 rounded bg-indigo-200 dark:bg-indigo-800/50 mb-3" />
                <div className="space-y-2">
                  <div className="h-3 w-full rounded bg-indigo-100 dark:bg-indigo-900/30" />
                  <div className="h-3 w-5/6 rounded bg-indigo-100 dark:bg-indigo-900/30" />
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </Section>
  );
}

