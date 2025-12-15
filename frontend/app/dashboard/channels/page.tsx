"use client";

import { useState } from "react";
import { Plus, Trash2, Save } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { PageHeader } from "@/components/ui/page-header";

type Channel = { id: string };

export default function ChannelsPage() {
  const [channels, setChannels] = useState<Channel[]>([
    { id: "UCawZsQWqfGSbCI5yjkdVkTA" },
  ]);
  const [input, setInput] = useState("");
  const [saving, setSaving] = useState(false);

  const addChannel = () => {
    if (!input.trim()) return;
    setChannels((prev) => [...prev, { id: input.trim() }]);
    setInput("");
  };

  const removeChannel = (id: string) => {
    setChannels((prev) => prev.filter((c) => c.id !== id));
  };

  const saveChannels = async () => {
    const BASE_URL = process.env.NEXT_PUBLIC_BASE_URL;
    setSaving(true);
    try {
      const res = await fetch(`${BASE_URL}/api/channels`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ channel_ids: channels.map((c) => c.id) }),
      });
      if (!res.ok) {
        throw new Error("Failed to save channels");
      }
    } catch (err) {
      console.error(err);
      alert("Failed to save channels. Please try again.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        badge="Channels"
        title="YouTube sources per user"
        subtitle="Users manage their own channel IDs (persisted in MongoDB). Backend should hydrate `YOUTUBE_CHANNELS` from these."
      />

      <Card padding="lg">
        <div className="space-y-4">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
            <div className="flex-1">
              <Input
                id="channel-input"
                placeholder="YouTube channel ID (e.g., UCawZsQWqfGSbCI5yjkdVkTA)"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault();
                    addChannel();
                  }
                }}
                aria-label="YouTube channel ID"
              />
            </div>
            <Button
              type="button"
              onClick={addChannel}
              variant="secondary"
              leftIcon={<Plus className="h-4 w-4" />}
              disabled={!input.trim()}
              aria-label="Add channel"
            >
              Add
            </Button>
          </div>

          <div className="divide-y divide-slate-200 dark:divide-[#2a2b31] rounded-lg border border-slate-200 dark:border-[#2a2b31] bg-white dark:bg-[#111216] overflow-hidden">
            {channels.length === 0 ? (
              <div className="px-4 py-8 text-center text-sm text-slate-500 dark:text-gray-400">
                No channels yet. Add at least one to receive digests.
              </div>
            ) : (
              channels.map((ch) => (
                <div
                  key={ch.id}
                  className="flex items-center justify-between px-4 py-3 text-sm text-slate-800 dark:text-gray-300 hover:bg-slate-50 dark:hover:bg-[#1a1b20] transition-colors"
                >
                  <span className="font-mono text-xs break-all">{ch.id}</span>
                  <Button
                    type="button"
                    onClick={() => removeChannel(ch.id)}
                    variant="ghost"
                    size="sm"
                    className="text-rose-600 dark:text-rose-400 hover:text-rose-700 dark:hover:text-rose-300 hover:bg-rose-50 dark:hover:bg-rose-950/20 shrink-0 ml-2"
                    aria-label={`Remove channel ${ch.id}`}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              ))
            )}
          </div>

          <Button
            type="button"
            onClick={saveChannels}
            variant="primary"
            size="lg"
            isLoading={saving}
            leftIcon={!saving ? <Save className="h-4 w-4" /> : undefined}
            disabled={channels.length === 0}
            aria-label="Save channels"
          >
            Save channels
          </Button>
        </div>
      </Card>
    </div>
  );
}
