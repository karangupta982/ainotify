"use client";

import { useEffect, useState } from "react";
import { CreditCard, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { PageHeader } from "@/components/ui/page-header";
import { Spinner } from "@/components/ui/spinner";

declare global {
  interface Window {
    Razorpay: any;
  }
}

const plans = [
  {
    name: "Starter",
    price: "₹200/mo",
    key: "starter",
    features: ["Daily digests", "Up to 10 channels"],
  },
  {
    name: "Pro",
    price: "₹500/mo",
    key: "pro",
    features: ["Priority LLM routing", "Up to 25 channels"],
  },
];

export default function BillingPage() {
  const [loadingPlan, setLoadingPlan] = useState<string | null>(null);
  const [currentPlan, setCurrentPlan] = useState("Trial (2 days)");
  const [razorpayReady, setRazorpayReady] = useState(false);
  const [loadingStatus, setLoadingStatus] = useState(true);
  const BASE_URL = process.env.NEXT_PUBLIC_BASE_URL;

  // Fetch current subscription status on mount
  useEffect(() => {
    fetchSubscriptionStatus();
  }, []);

  const fetchSubscriptionStatus = async () => {
    try {
      const res = await fetch(`${BASE_URL}/api/billing/status`, {
        method: "GET",
        credentials: "include",
      });
      if (res.ok) {
        const data = await res.json();
        setCurrentPlan(data.display_name || "Trial (2 days)");
      }
    } catch (err) {
      console.error("Failed to fetch subscription status:", err);
    } finally {
      setLoadingStatus(false);
    }
  };

  useEffect(() => {
    const script = document.createElement("script");
    script.src = "https://checkout.razorpay.com/v1/checkout.js";
    script.async = true;
    script.onload = () => setRazorpayReady(true);
    document.body.appendChild(script);

    return () => {
      const existingScript = document.querySelector(
        'script[src="https://checkout.razorpay.com/v1/checkout.js"]'
      );
      if (existingScript) {
        existingScript.remove();
      }
    };
  }, []);

  const verifyPayment = async (
    paymentId: string,
    orderId: string,
    signature: string
  ) => {
    try {
      const res = await fetch(`${BASE_URL}/api/billing/verify-payment`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          razorpay_payment_id: paymentId,
          razorpay_order_id: orderId,
          razorpay_signature: signature,
        }),
        credentials: "include",
      });

      if (!res.ok) {
        const error = await res.json().catch(() => ({}));
        throw new Error(error.detail || "Payment verification failed");
      }

      const data = await res.json();
      // Refresh subscription status after successful verification
      await fetchSubscriptionStatus();
      return data;
    } catch (err: any) {
      console.error("Payment verification error:", err);
      throw err;
    }
  };

  const startCheckout = async (planKey: string) => {
    // CRITICAL FIX: Prevent double-click by checking if already loading
    // Each button has its own handler bound to the specific plan key
    if (loadingPlan !== null || !razorpayReady) {
      if (!razorpayReady) {
        alert("Razorpay is loading, please wait a moment.");
      }
      return;
    }

    setLoadingPlan(planKey);
    try {
      const res = await fetch(`${BASE_URL}/api/billing/checkout`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ priceId: planKey }),
        credentials: "include",
      });

      if (!res.ok) {
        throw new Error("Failed to initiate checkout");
      }

      const data = await res.json();
      if (data.order_id && data.key_id) {
        const options = {
          key: data.key_id,
          amount: data.amount,
          currency: data.currency,
          name: "AI Notify",
          description: `Subscription - ${planKey}`,
          order_id: data.order_id,
          handler: async function (response: any) {
            try {
              console.log("Payment success", response);
              // Verify payment and update subscription
              await verifyPayment(
                response.razorpay_payment_id,
                response.razorpay_order_id,
                response.razorpay_signature
              );
              alert(`Payment successful! Your subscription has been upgraded to ${planKey}.`);
              setLoadingPlan(null);
            } catch (err: any) {
              console.error("Payment verification failed:", err);
              alert(
                err.message ||
                  "Payment succeeded but verification failed. Please contact support."
              );
              setLoadingPlan(null);
            }
          },
          prefill: {},
          notes: { plan: planKey },
          theme: { color: "#4f46e5" },
        };
        const rz = new window.Razorpay(options);
        rz.on("payment.failed", function (response: any) {
          console.error("Payment failed", response);
          alert(
            `Payment failed: ${response.error?.description || "Unknown error"}`
          );
          setLoadingPlan(null);
        });
        rz.on("payment.error", function (response: any) {
          console.error("Payment error", response);
          alert(`Payment error: ${response.error?.description || "Unknown error"}`);
          setLoadingPlan(null);
        });
        rz.open();
      } else {
        throw new Error("Invalid response from server");
      }
    } catch (err: any) {
      console.error(err);
      alert(err.message || "Failed to start checkout. Please try again.");
      setLoadingPlan(null);
    }
  };

  if (loadingStatus) {
    return (
      <div className="space-y-6">
        <PageHeader
          badge="Billing"
          title="Subscription"
          subtitle="2-day free tier, then pick a plan via Razorpay Checkout."
        />
        <Spinner centered text="Loading subscription status..." />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader
        badge="Billing"
        title="Subscription"
        subtitle="2-day free tier, then pick a plan via Razorpay Checkout."
      />

      <Card padding="md" hover>
        <div className="flex items-center gap-3">
          <ShieldCheck
            className="h-5 w-5 text-emerald-500 dark:text-emerald-400 shrink-0"
            aria-hidden="true"
          />
          <div>
            <div className="text-sm font-medium text-slate-800 dark:text-gray-300">
              Current status:{" "}
              <span className="font-semibold">{currentPlan}</span>
            </div>
          </div>
        </div>
      </Card>

      <div className="grid gap-4 sm:grid-cols-2">
        {plans.map((plan) => {
          const isLoading = loadingPlan === plan.key;
          const isDisabled = loadingPlan !== null;

          return (
            <Card
              key={plan.name}
              padding="lg"
              hover
              className={`flex flex-col ${
                isLoading
                  ? "ring-2 ring-indigo-500 dark:ring-indigo-400 dark:shadow-[0_0_20px_rgba(99,102,241,0.3)]"
                  : ""
              }`}
            >
              <div className="flex items-center justify-between mb-4">
                <div>
                  <div className="text-lg font-semibold text-slate-900 dark:text-white">
                    {plan.name}
                  </div>
                  <div className="text-sm text-slate-600 dark:text-gray-400">
                    {plan.price}
                  </div>
                </div>
                <CreditCard
                  className="h-5 w-5 text-indigo-600 dark:text-indigo-400 shrink-0"
                  aria-hidden="true"
                />
              </div>
              <ul className="space-y-2 text-sm text-slate-700 dark:text-gray-300 mb-6 flex-1">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start gap-2">
                    <span className="text-indigo-600 dark:text-indigo-400 mt-0.5">
                      •
                    </span>
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
              <Button
                type="button"
                onClick={() => startCheckout(plan.key)}
                disabled={isDisabled}
                isLoading={isLoading}
                variant="primary"
                size="lg"
                className="w-full mt-auto"
                aria-label={`Choose ${plan.name} plan`}
              >
                {isLoading ? "Processing..." : "Choose plan"}
              </Button>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
