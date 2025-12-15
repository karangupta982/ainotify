"use client";

import { Sparkles, Zap, ShieldCheck } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Section } from "@/components/ui/section";

const features = [
  {
    icon: Sparkles,
    title: "Daily AI Digests",
    description:
      "YouTube + OpenAI + Anthropic news, summarized to your persona. Get the most relevant AI developments delivered to your inbox every morning.",
    gradient: "from-indigo-500 to-purple-500",
  },
  {
    icon: Zap,
    title: "LLM-Powered Curation",
    description:
      "Ranked to your interests, delivered to your inbox automatically. Our advanced LLMs understand context and prioritize what matters to you.",
    gradient: "from-amber-500 to-orange-500",
  },
  {
    icon: ShieldCheck,
    title: "Secure by Default",
    description:
      "JWT auth, httpOnly cookies, Razorpay billing, and role-based access. Enterprise-grade security without the enterprise complexity.",
    gradient: "from-emerald-500 to-teal-500",
  },
];

export function Features() {
  return (
    <div className="bg-slate-50 dark:bg-[#0d0d11]">
      <Section
        title="Everything you need"
        description="Built for professionals who want to stay ahead without the noise."
        spacing="lg"
        className="py-24"
      >
      <div className="grid gap-6 md:grid-cols-3">
        {features.map((feature, index) => {
          const Icon = feature.icon;
          return (
            <Card
              key={feature.title}
              padding="lg"
              hover
              className="group relative overflow-hidden animate-fade-in bg-white dark:bg-[#111216]"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              {/* Gradient background on hover */}
              <div
                className={`absolute inset-0 bg-gradient-to-br ${feature.gradient} opacity-0 group-hover:opacity-5 dark:group-hover:opacity-10 transition-opacity`}
              />

              <div className="relative space-y-4">
                {/* Icon */}
                <div
                  className={`inline-flex h-14 w-14 items-center justify-center rounded-xl bg-gradient-to-br ${feature.gradient} text-white shadow-lg group-hover:scale-110 transition-transform`}
                >
                  <Icon className="h-7 w-7" />
                </div>

                {/* Content */}
                <div className="space-y-2">
                  <h3 className="text-2xl font-semibold text-slate-900 dark:text-white">
                    {feature.title}
                  </h3>
                  <p className="text-base text-gray-600 dark:text-gray-300 leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              </div>
            </Card>
          );
        })}
      </div>
      </Section>
    </div>
  );
}

