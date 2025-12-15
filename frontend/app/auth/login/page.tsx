"use client";

import Link from "next/link";
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const BASE_URL = process.env.NEXT_PUBLIC_BASE_URL;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${BASE_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
        credentials: "include",
      });
      if (!res.ok) {
        throw new Error("Invalid credentials");
      }
      window.location.href = "/dashboard";
    } catch (err: any) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card padding="lg" className="w-full max-w-xl shadow-xl dark:shadow-[0_0_40px_rgba(99,102,241,0.1)] animate-fade-in">
      <div className="mb-8 space-y-2 text-center">
        <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600 dark:text-indigo-400">
          Welcome back
        </p>
        <h1 className="text-4xl font-semibold text-slate-900 dark:text-white leading-tight">
          Sign in
        </h1>
        <p className="text-base text-gray-600 dark:text-gray-300 leading-relaxed">
          Access your AI digests dashboard.
        </p>
      </div>

      <form className="space-y-5" onSubmit={handleSubmit} noValidate>
        <Input
          id="email"
          type="email"
          label="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          error={error && error.includes("email") ? error : undefined}
          autoComplete="email"
          aria-label="Email address"
        />
        <Input
          id="password"
          type="password"
          label="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          error={error && error.includes("password") ? error : undefined}
          autoComplete="current-password"
          aria-label="Password"
        />
        {error && !error.includes("email") && !error.includes("password") && (
          <div
            className="rounded-lg border border-rose-200 dark:border-rose-800 bg-rose-50 dark:bg-rose-950/20 px-4 py-3 text-sm text-rose-700 dark:text-rose-400"
            role="alert"
          >
            {error}
          </div>
        )}
        <Button
          type="submit"
          variant="primary"
          size="lg"
          isLoading={loading}
          className="w-full"
          aria-label="Sign in to your account"
        >
          Sign in
        </Button>
      </form>

      <p className="mt-6 text-center text-base text-gray-600 dark:text-gray-300">
        New here?{" "}
        <Link
          href="/auth/signup"
          className="font-semibold text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 transition-colors cursor-pointer focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 rounded"
          aria-label="Create a new account"
        >
          Create an account
        </Link>
      </p>
    </Card>
  );
}
