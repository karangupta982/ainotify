"use client";

import Link from "next/link";
import { Github, Twitter, Linkedin } from "lucide-react";

const links = {
  product: [
    { label: "Dashboard", href: "/dashboard" },
    { label: "Pricing", href: "/dashboard/billing" },
    { label: "Features", href: "#features" },
  ],
  company: [
    { label: "About", href: "#" },
    { label: "Blog", href: "#" },
    { label: "Careers", href: "#" },
  ],
  legal: [
    { label: "Terms", href: "#" },
    { label: "Privacy", href: "#" },
    { label: "Security", href: "#" },
  ],
  resources: [
    { label: "Documentation", href: "#" },
    { label: "Support", href: "#" },
    { label: "Contact", href: "#" },
  ],
};

const socials = [
  { icon: Github, href: "#", label: "GitHub" },
  { icon: Twitter, href: "#", label: "Twitter" },
  { icon: Linkedin, href: "#", label: "LinkedIn" },
];

export function Footer() {
  return (
    <footer className="border-t border-slate-200 dark:border-[#2a2b31] bg-white dark:bg-[#0d0d11]">
      <div className="mx-auto max-w-7xl px-6 md:px-12 lg:px-24 py-12 md:py-16">
        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-6">
          {/* Brand */}
          <div className="lg:col-span-2 space-y-4">
            <div className="text-lg font-semibold text-slate-900 dark:text-white">
              AI Notify
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 max-w-xs">
              Personalized AI news digests tailored to your interests and
              expertise level.
            </p>
            {/* Social Links */}
            <div className="flex items-center gap-4">
              {socials.map((social) => {
                const Icon = social.icon;
                return (
                  <Link
                    key={social.label}
                    href={social.href}
                    className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
                    aria-label={social.label}
                  >
                    <Icon className="h-5 w-5" />
                  </Link>
                );
              })}
            </div>
          </div>

          {/* Links */}
          <div>
            <h4 className="text-sm font-semibold text-slate-900 dark:text-white mb-4">
              Product
            </h4>
            <ul className="space-y-3">
              {links.product.map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    className="text-sm text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-slate-900 dark:text-white mb-4">
              Company
            </h4>
            <ul className="space-y-3">
              {links.company.map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    className="text-sm text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-slate-900 dark:text-white mb-4">
              Legal
            </h4>
            <ul className="space-y-3">
              {links.legal.map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    className="text-sm text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-slate-900 dark:text-white mb-4">
              Resources
            </h4>
            <ul className="space-y-3">
              {links.resources.map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    className="text-sm text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-8 border-t border-slate-200 dark:border-[#2a2b31] flex flex-col sm:flex-row justify-between items-center gap-4">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            © {new Date().getFullYear()} AI Notify. All rights reserved.
          </p>
          <div className="flex items-center gap-6">
            <Link
              href="#"
              className="text-sm text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
            >
              Status
            </Link>
            <Link
              href="#"
              className="text-sm text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
            >
              Changelog
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}

