"use client";

import { User, Youtube, Sparkles, CreditCard } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Section } from "@/components/ui/section";

const steps = [
  {
    number: "01",
    icon: User,
    title: "Create your profile",
    description:
      "Define your interests, expertise level, and email target. Our system uses this to personalize your digest experience.",
  },
  {
    number: "02",
    icon: Youtube,
    title: "Add YouTube channels",
    description:
      "Connect your favorite YouTube channels and RSS feeds. We automatically scrape and store content for processing.",
  },
  {
    number: "03",
    icon: Sparkles,
    title: "AI-powered curation",
    description:
      "Our LLMs summarize, rank, and curate content daily based on your profile. You get only what matters to you.",
  },
  {
    number: "04",
    icon: CreditCard,
    title: "Upgrade seamlessly",
    description:
      "Start with a 2-day free tier, then upgrade via Razorpay checkout. No credit card required for trial.",
  },
];

export function HowItWorks() {
  return (
    <Section
      title="How it works"
      description="Get started in minutes and receive your first digest within 24 hours."
      spacing="lg"
      className="py-24"
    >
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {steps.map((step, index) => {
          const Icon = step.icon;
          return (
            <Card
              key={step.number}
              padding="lg"
              hover
              className="group relative overflow-hidden animate-fade-in"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              {/* Number badge */}
              <div className="absolute top-4 right-4 text-6xl font-black text-slate-100 dark:text-slate-800/50 group-hover:text-indigo-100 dark:group-hover:text-indigo-900/30 transition-colors">
                {step.number}
              </div>

              <div className="relative space-y-4">
                {/* Icon */}
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-100 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400 group-hover:scale-110 transition-transform">
                  <Icon className="h-6 w-6" />
                </div>

                {/* Content */}
                <div className="space-y-2">
                  <h3 className="text-xl font-semibold text-slate-900 dark:text-white">
                    {step.title}
                  </h3>
                  <p className="text-base text-gray-600 dark:text-gray-300 leading-relaxed">
                    {step.description}
                  </p>
                </div>
              </div>
            </Card>
          );
        })}
      </div>
    </Section>
  );
}

