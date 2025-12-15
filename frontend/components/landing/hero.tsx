"use client";

import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Hero() {
  return (
    <section className="relative overflow-hidden py-24 md:py-32">
      {/* Background gradients */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute left-1/4 top-0 h-96 w-96 rounded-full bg-indigo-500/20 blur-3xl dark:bg-indigo-500/10" />
        <div className="absolute right-1/4 bottom-0 h-96 w-96 rounded-full bg-purple-500/20 blur-3xl dark:bg-purple-500/10" />
      </div>

      <div className="mx-auto max-w-7xl px-6 md:px-12 lg:px-24">
        <div className="grid gap-12 lg:grid-cols-2 lg:gap-16 lg:items-center">
          {/* Left Content */}
          <div className="space-y-8 animate-fade-in">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 rounded-full border border-indigo-100 dark:border-indigo-900/50 bg-indigo-50 dark:bg-indigo-950/30 px-4 py-2 text-xs font-semibold text-indigo-700 dark:text-indigo-400">
              <span>AI Notify</span>
              <span className="text-indigo-400 dark:text-indigo-600">·</span>
              <span>Personalized AI news SaaS</span>
            </div>

            {/* Headline */}
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-semibold tracking-tight text-slate-900 dark:text-white leading-tight">
              Stay ahead of AI{" "}
              <span className="block">
                with a{" "}
                <span className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 dark:from-indigo-400 dark:via-purple-400 dark:to-pink-400 bg-clip-text text-transparent">
                  daily, curated digest
                </span>
                .
              </span>
            </h1>

            {/* Subheading */}
            <p className="text-xl text-gray-600 dark:text-gray-300 leading-relaxed max-w-2xl">
              Connect your interests and channels, let our LLMs summarize and
              rank, and receive polished email updates—free for 2 days, then
              keep the signal flowing with a paid plan.
            </p>

            {/* CTAs */}
            <div className="flex flex-wrap items-center gap-4">
              <Button
                asChild
                href="/auth/signup"
                variant="primary"
                size="lg"
                rightIcon={<ArrowRight className="h-4 w-4" />}
              >
                Get started free
              </Button>
              <Button asChild href="/auth/login" variant="secondary" size="lg">
                Sign in
              </Button>
            </div>

            {/* Status Indicators */}
            <div className="flex flex-wrap items-center gap-6 pt-4">
              <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-gray-400">
                <div className="h-2.5 w-2.5 rounded-full bg-emerald-500 dark:bg-emerald-400" />
                <span>Uptime monitored</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-gray-400">
                <div className="h-2.5 w-2.5 rounded-full bg-indigo-500 dark:bg-indigo-400" />
                <span>LLM summaries + ranking</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-gray-400">
                <div className="h-2.5 w-2.5 rounded-full bg-amber-500 dark:bg-amber-400" />
                <span>Razorpay billing</span>
              </div>
            </div>
          </div>

          {/* Right Side - UI Mockup */}
          <div className="relative lg:pl-8">
            <div className="relative rounded-2xl border border-slate-200 dark:border-[#2a2b31] bg-white dark:bg-[#111216] shadow-2xl dark:shadow-[0_0_60px_rgba(99,102,241,0.15)] overflow-hidden">
              {/* Mockup Header */}
              <div className="flex items-center gap-2 border-b border-slate-200 dark:border-[#2a2b31] bg-slate-50 dark:bg-[#1a1b20] px-4 py-3">
                <div className="flex gap-1.5">
                  <div className="h-3 w-3 rounded-full bg-red-400" />
                  <div className="h-3 w-3 rounded-full bg-amber-400" />
                  <div className="h-3 w-3 rounded-full bg-emerald-400" />
                </div>
                <div className="flex-1 text-center">
                  <span className="text-xs font-medium text-slate-600 dark:text-gray-400">
                    AI Notify Dashboard
                  </span>
                </div>
              </div>

              {/* Mockup Content */}
              <div className="p-6 space-y-4">
                {/* Email Preview Card */}
                <div className="rounded-lg border border-slate-200 dark:border-[#2a2b31] bg-gradient-to-br from-indigo-50 to-purple-50 dark:from-indigo-950/30 dark:to-purple-950/30 p-4">
                  <div className="flex items-start gap-3">
                    <div className="h-10 w-10 rounded-full bg-indigo-600 dark:bg-indigo-500 flex items-center justify-center">
                      <span className="text-white text-sm font-semibold">AI</span>
                    </div>
                    <div className="flex-1 space-y-2">
                      <div className="h-3 w-3/4 rounded bg-indigo-200 dark:bg-indigo-800/50" />
                      <div className="h-2 w-full rounded bg-slate-200 dark:bg-slate-700" />
                      <div className="h-2 w-5/6 rounded bg-slate-200 dark:bg-slate-700" />
                    </div>
                  </div>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-3 gap-3">
                  {[1, 2, 3].map((i) => (
                    <div
                      key={i}
                      className="rounded-lg border border-slate-200 dark:border-[#2a2b31] bg-white dark:bg-[#1a1b20] p-3"
                    >
                      <div className="h-2 w-2/3 rounded bg-slate-200 dark:bg-slate-700 mb-2" />
                      <div className="h-4 w-1/2 rounded bg-indigo-200 dark:bg-indigo-800/50" />
                    </div>
                  ))}
                </div>

                {/* Channel List */}
                <div className="space-y-2">
                  {[1, 2, 3].map((i) => (
                    <div
                      key={i}
                      className="flex items-center gap-3 rounded-lg border border-slate-200 dark:border-[#2a2b31] bg-white dark:bg-[#1a1b20] p-3"
                    >
                      <div className="h-8 w-8 rounded-full bg-slate-200 dark:bg-slate-700" />
                      <div className="flex-1 space-y-1.5">
                        <div className="h-2 w-3/4 rounded bg-slate-200 dark:bg-slate-700" />
                        <div className="h-2 w-1/2 rounded bg-slate-200 dark:bg-slate-700" />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Decorative elements */}
            <div className="absolute -z-10 -right-4 -bottom-4 h-64 w-64 rounded-full bg-indigo-500/10 dark:bg-indigo-500/5 blur-3xl" />
            <div className="absolute -z-10 -left-4 -top-4 h-48 w-48 rounded-full bg-purple-500/10 dark:bg-purple-500/5 blur-3xl" />
          </div>
        </div>
      </div>
    </section>
  );
}

