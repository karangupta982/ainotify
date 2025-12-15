"use client";

import { ThemeToggle } from "@/components/ui/theme-toggle";
import { Hero } from "@/components/landing/hero";
import { HowItWorks } from "@/components/landing/how-it-works";
import { Features } from "@/components/landing/features";
import { Showcase } from "@/components/landing/showcase";
import { PricingTeaser } from "@/components/landing/pricing-teaser";
import { Testimonials } from "@/components/landing/testimonials";
import { Footer } from "@/components/landing/footer";

export default function Home() {
  return (
    <div className="min-h-screen bg-white dark:bg-[#0d0d11] transition-colors duration-200">
      {/* Theme Toggle - Fixed Position */}
      <div className="fixed top-6 right-6 z-50">
        <ThemeToggle />
            </div>

      {/* Hero Section */}
      <Hero />

      {/* How It Works */}
      <HowItWorks />

      {/* Features */}
      <Features />

      {/* Showcase */}
      <Showcase />

      {/* Pricing Teaser */}
      <PricingTeaser />

      {/* Testimonials */}
      <Testimonials />

      {/* Final CTA Section */}
      <section className="py-24 bg-gradient-to-br from-indigo-600 to-purple-600 dark:from-indigo-700 dark:to-purple-700">
        <div className="mx-auto max-w-7xl px-6 md:px-12 lg:px-24">
          <div className="mx-auto max-w-4xl text-center">
          <h2 className="text-3xl md:text-4xl font-semibold text-white mb-4 leading-tight">
            Ready to stay ahead of AI?
          </h2>
          <p className="text-xl text-indigo-100 mb-8 max-w-2xl mx-auto">
            Join thousands of professionals who get personalized AI news
            delivered daily. Start your free trial today.
            </p>
          <div className="flex flex-wrap items-center justify-center gap-4">
            <a
              href="/auth/signup"
              className="inline-flex items-center justify-center gap-2 rounded-lg bg-white px-6 py-3 text-base font-semibold text-indigo-600 shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-200 cursor-pointer"
            >
                Get started free
            </a>
            <a
              href="/auth/login"
              className="inline-flex items-center justify-center gap-2 rounded-lg border-2 border-white/20 bg-white/10 backdrop-blur-sm px-6 py-3 text-base font-semibold text-white hover:bg-white/20 transition-all duration-200 cursor-pointer"
            >
                Sign in
            </a>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <Footer />
      </div>
  );
}
