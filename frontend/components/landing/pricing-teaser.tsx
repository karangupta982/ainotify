"use client";

import { ArrowRight, Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Section } from "@/components/ui/section";
import Link from "next/link";

const plans = [
  {
    name: "Starter",
    price: "₹200",
    period: "/month",
    description: "Perfect for individuals",
    features: [
      "Daily AI digests",
      "Up to 10 channels",
      "Email delivery",
      "Basic customization",
    ],
    highlight: false,
  },
  {
    name: "Pro",
    price: "₹500",
    period: "/month",
    description: "For power users and teams",
    features: [
      "Priority LLM routing",
      "Up to 25 channels",
      "Advanced filtering",
      "Priority support",
    ],
    highlight: true,
  },
];

export function PricingTeaser() {
  return (
    <div className="bg-slate-50 dark:bg-[#0d0d11]">
      <Section
        title="Simple, transparent pricing"
        description="Start free for 2 days, then choose the plan that works for you."
        spacing="lg"
        className="py-24"
      >
      <div className="grid gap-6 md:grid-cols-2 max-w-4xl mx-auto">
        {plans.map((plan) => (
          <Card
            key={plan.name}
            padding="lg"
            hover
            className={`relative overflow-hidden ${
              plan.highlight
                ? "ring-2 ring-indigo-500 dark:ring-indigo-400 shadow-xl dark:shadow-[0_0_40px_rgba(99,102,241,0.2)]"
                : ""
            }`}
          >
            {plan.highlight && (
              <div className="absolute top-0 right-0 bg-indigo-600 dark:bg-indigo-500 text-white text-xs font-semibold px-3 py-1 rounded-bl-lg">
                Popular
              </div>
            )}

            <div className="space-y-6">
              {/* Header */}
              <div>
                <h3 className="text-2xl font-semibold text-slate-900 dark:text-white mb-2">
                  {plan.name}
                </h3>
                <p className="text-base text-gray-600 dark:text-gray-300 mb-4">
                  {plan.description}
                </p>
                <div className="flex items-baseline gap-1">
                  <span className="text-4xl font-bold text-slate-900 dark:text-white">
                    {plan.price}
                  </span>
                  <span className="text-base text-gray-600 dark:text-gray-400">
                    {plan.period}
                  </span>
                </div>
              </div>

              {/* Features */}
              <ul className="space-y-3">
                {plan.features.map((feature) => (
                  <li
                    key={feature}
                    className="flex items-start gap-3 text-base text-gray-600 dark:text-gray-300"
                  >
                    <Check className="h-5 w-5 text-indigo-600 dark:text-indigo-400 shrink-0 mt-0.5" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>

              {/* CTA */}
              <Button
                asChild
                href="/dashboard/billing"
                variant={plan.highlight ? "primary" : "secondary"}
                size="lg"
                className="w-full"
                rightIcon={<ArrowRight className="h-4 w-4" />}
              >
                {plan.highlight ? "Get started" : "View details"}
              </Button>
            </div>
          </Card>
        ))}
      </div>

      {/* Footer CTA */}
      <div className="text-center mt-12">
        <p className="text-base text-gray-600 dark:text-gray-300 mb-4">
          All plans include a 2-day free trial. No credit card required.
        </p>
        <Button
          asChild
          href="/dashboard/billing"
          variant="ghost"
          size="md"
        >
          View detailed pricing
        </Button>
      </div>
      </Section>
    </div>
  );
}

