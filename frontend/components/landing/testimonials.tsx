"use client";

import { Card } from "@/components/ui/card";
import { Section } from "@/components/ui/section";
import { Quote } from "lucide-react";

const testimonials = [
  {
    name: "Sarah Chen",
    role: "AI Research Lead",
    company: "TechCorp",
    avatar: "SC",
    quote:
      "AI Notify has transformed how I stay updated. The personalized digests save me hours every week, and the quality of curation is exceptional.",
  },
  {
    name: "Michael Rodriguez",
    role: "Product Manager",
    company: "StartupXYZ",
    avatar: "MR",
    quote:
      "Finally, a tool that understands what I actually care about. The LLM-powered ranking is spot-on, and I never miss important developments anymore.",
  },
  {
    name: "Emily Watson",
    role: "ML Engineer",
    company: "DataFlow",
    avatar: "EW",
    quote:
      "The daily digests are perfectly tailored to my expertise level. It's like having a research assistant who knows exactly what I need to know.",
  },
];

export function Testimonials() {
  return (
    <Section
      title="Loved by professionals"
      description="Join thousands of users who stay ahead with AI Notify."
      spacing="lg"
      className="py-24"
    >
      <div className="grid gap-6 md:grid-cols-3">
        {testimonials.map((testimonial, index) => (
          <Card
            key={testimonial.name}
            padding="lg"
            hover
            className="animate-fade-in"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <div className="space-y-4">
              {/* Quote Icon */}
              <div className="text-indigo-600 dark:text-indigo-400">
                <Quote className="h-8 w-8" />
              </div>

              {/* Quote */}
              <p className="text-base text-gray-600 dark:text-gray-300 leading-relaxed">
                "{testimonial.quote}"
              </p>

              {/* Author */}
              <div className="flex items-center gap-3 pt-4 border-t border-slate-200 dark:border-[#2a2b31]">
                <div className="h-10 w-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-white font-semibold text-sm">
                  {testimonial.avatar}
                </div>
                <div>
                  <div className="text-sm font-semibold text-slate-900 dark:text-white">
                    {testimonial.name}
                  </div>
                  <div className="text-xs text-gray-600 dark:text-gray-400">
                    {testimonial.role} at {testimonial.company}
                  </div>
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </Section>
  );
}

