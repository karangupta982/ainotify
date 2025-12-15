"use client";

import { useEffect, useState } from "react";
import { Mail, ListChecks, Clock3, BellRing } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Spinner } from "@/components/ui/spinner";
import { PageHeader } from "@/components/ui/page-header";
import { Section } from "@/components/ui/section";

type Stats = {
  digestsToday: number;
  channels: number;
  profileComplete: boolean;
  trialEndsAt?: string;
};

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // TODO: Replace with real API call
    setTimeout(() => {
      setStats({
        digestsToday: 3,
        channels: 5,
        profileComplete: true,
        trialEndsAt: new Date(Date.now() + 36 * 3600 * 1000).toISOString(),
      });
      setLoading(false);
    }, 500);
  }, []);

  if (loading || !stats) {
    return <Spinner centered text="Loading dashboard..." />;
  }

  return (
    <div className="space-y-6">
      <PageHeader
        badge="Dashboard"
        title="Welcome back to AI Notify"
        subtitle="Your personalized AI digest status and billing overview."
      />

      <Section spacing="md">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <StatCard
            title="Digests sent today"
            value={stats.digestsToday}
            icon={<Mail className="h-5 w-5 text-indigo-600 dark:text-indigo-400" />}
          />
          <StatCard
            title="YouTube channels"
            value={stats.channels}
            icon={<BellRing className="h-5 w-5 text-amber-500 dark:text-amber-400" />}
          />
          <StatCard
            title="Profile completeness"
            value={stats.profileComplete ? "Ready" : "Incomplete"}
            icon={<ListChecks className="h-5 w-5 text-emerald-500 dark:text-emerald-400" />}
          />
        </div>
      </Section>

      <Card padding="md" hover>
        <div className="flex items-center gap-3">
          <Clock3
            className="h-5 w-5 text-indigo-600 dark:text-indigo-400 flex-shrink-0"
            aria-hidden="true"
          />
          <div>
            <div className="text-sm font-semibold text-slate-900 dark:text-white">
              Free tier status
            </div>
            <div className="text-sm text-slate-600 dark:text-gray-400">
              {stats.trialEndsAt
                ? `Trial ends ${new Date(stats.trialEndsAt).toLocaleString()}`
                : "Start your 2-day free tier to receive digests."}
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}

function StatCard({
  title,
  value,
  icon,
}: {
  title: string;
  value: string | number;
  icon: React.ReactNode;
}) {
  return (
    <Card padding="md" hover>
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-indigo-50 dark:bg-indigo-950/30">
          {icon}
        </div>
        <div>
          <div className="text-sm font-medium text-slate-600 dark:text-gray-400">
            {title}
          </div>
          <div className="text-2xl font-semibold text-slate-900 dark:text-white">
            {value}
          </div>
        </div>
      </div>
    </Card>
  );
}
