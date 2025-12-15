"use client";

import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { PageHeader } from "@/components/ui/page-header";
import { Section } from "@/components/ui/section";
import { Save, CheckCircle2 } from "lucide-react";

type Preferences = {
  prefer_practical: boolean;
  prefer_technical_depth: boolean;
  prefer_research_breakthroughs: boolean;
  prefer_production_focus: boolean;
  avoid_marketing_hype: boolean;
};

type ProfilePayload = {
  name: string;
  title: string;
  email_to: string;
  background: string;
  interests: string;
  expertise_level: string;
  preferences: Preferences;
};

const defaultProfile: ProfilePayload = {
  name: "",
  title: "",
  email_to: "",
  background: "",
  interests: "",
  expertise_level: "Intermediate",
  preferences: {
    prefer_practical: true,
    prefer_technical_depth: true,
    prefer_research_breakthroughs: true,
    prefer_production_focus: true,
    avoid_marketing_hype: true,
  },
};

export default function ProfilePage() {
  const [profile, setProfile] = useState<ProfilePayload>(defaultProfile);
  const [loading, setLoading] = useState(false);
  const [saved, setSaved] = useState(false);
  const BASE_URL = process.env.NEXT_PUBLIC_BASE_URL;

  useEffect(() => {
    // TODO: Load from backend
    setProfile((p) => ({
      ...p,
      name: "Karan",
      title: "Software Engineer",
      email_to: "gupta.karan1.gh@gmail.com",
      background:
        "Experienced Software engineer with deep interest in practical AI applications, research breakthroughs, and production-ready systems",
      interests:
        "Large Language Models (LLMs) and their applications, Retrieval-Augmented Generation (RAG) systems, AI agent architectures and frameworks, Multimodal AI and vision-language models, AI safety and alignment research, Production AI systems and MLOps, Real-world AI applications and case studies, Technical tutorials and implementation guides, Research papers with practical implications, AI infrastructure and scaling challenges",
      expertise_level: "Advanced",
    }));
  }, []);

  const saveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setSaved(false);
    try {
      const res = await fetch(`${BASE_URL}/api/profile`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(profile),
        credentials: "include",
      });
      if (!res.ok) throw new Error("Save failed");
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        badge="Profile"
        title="User persona"
        subtitle="This data feeds the curator and email agents and sets the email delivery target."
      />

      <Card padding="lg">
        <form onSubmit={saveProfile} className="space-y-6" noValidate>
          <Section title="Basic Information" spacing="sm">
            <div className="grid gap-4 sm:grid-cols-2">
              <Input
                id="name"
                label="Name"
                value={profile.name}
                onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                required
                autoComplete="name"
              />
              <Input
                id="title"
                label="Title"
                value={profile.title}
                onChange={(e) =>
                  setProfile({ ...profile, title: e.target.value })
                }
                required
                autoComplete="organization-title"
              />
              <Input
                id="email_to"
                type="email"
                label="Digest recipient email"
                value={profile.email_to}
                onChange={(e) =>
                  setProfile({ ...profile, email_to: e.target.value })
                }
                required
                hint="Where daily digests are sent (stored in backend user profile)."
                autoComplete="email"
              />
              <label className="flex flex-col gap-2 text-sm font-medium text-slate-800 dark:text-gray-300">
                <span>Expertise level</span>
                <select
                  value={profile.expertise_level}
                  onChange={(e) =>
                    setProfile({ ...profile, expertise_level: e.target.value })
                  }
                  className="w-full h-12 rounded-lg border border-slate-200 dark:border-[#2a2b31] bg-white dark:bg-[#111216] px-4 py-2 text-sm text-slate-900 dark:text-gray-200 shadow-sm transition-colors hover:border-slate-300 dark:hover:border-[#3a3b41] focus:border-indigo-500 dark:focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 dark:focus:ring-indigo-500/30 cursor-pointer"
                  aria-label="Expertise level"
                >
                  <option value="Beginner">Beginner</option>
                  <option value="Intermediate">Intermediate</option>
                  <option value="Advanced">Advanced</option>
                </select>
              </label>
            </div>
          </Section>

          <Section title="Background & Interests" spacing="sm">
            <Input
              id="background"
              as="textarea"
              label="Background"
              value={profile.background}
              onChange={(e) =>
                setProfile({ ...profile, background: e.target.value })
              }
              rows={3}
              hint="Helps ranking prioritize depth and style."
            />

            <Input
              id="interests"
              label="Interests (comma-separated)"
              value={profile.interests}
              onChange={(e) =>
                setProfile({ ...profile, interests: e.target.value })
              }
              hint="e.g. LLMs, RAG, agents, multimodal, safety, MLOps"
            />
          </Section>

          <Section title="Preferences" spacing="sm">
            <div className="grid gap-3 sm:grid-cols-2">
              {Object.entries(profile.preferences).map(([key, val]) => (
                <label
                  key={key}
                  className="flex items-center justify-between rounded-lg border border-slate-200 dark:border-[#2a2b31] bg-white dark:bg-[#111216] px-3 py-2.5 text-sm text-slate-800 dark:text-gray-300 transition-colors hover:bg-slate-50 dark:hover:bg-[#1a1b20] cursor-pointer"
                >
                  <span className="capitalize">{key.replaceAll("_", " ")}</span>
                  <input
                    type="checkbox"
                    checked={val}
                    onChange={(e) =>
                      setProfile({
                        ...profile,
                        preferences: {
                          ...profile.preferences,
                          [key]: e.target.checked,
                        },
                      })
                    }
                    className="h-4 w-4 accent-indigo-600 dark:accent-indigo-500 cursor-pointer"
                    aria-label={key.replaceAll("_", " ")}
                  />
                </label>
              ))}
            </div>
          </Section>

          <div className="flex items-center gap-4 pt-4">
            <Button
              type="submit"
              variant="primary"
              size="lg"
              isLoading={loading}
              leftIcon={!loading ? <Save className="h-4 w-4" /> : undefined}
              aria-label="Save profile"
            >
              Save profile
            </Button>
            {saved && (
              <div
                className="flex items-center gap-2 text-sm text-emerald-600 dark:text-emerald-400"
                role="status"
                aria-live="polite"
              >
                <CheckCircle2 className="h-4 w-4" />
                <span>Profile saved</span>
              </div>
            )}
          </div>
        </form>
      </Card>
    </div>
  );
}
