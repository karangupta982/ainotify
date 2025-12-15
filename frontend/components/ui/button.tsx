"use client";

import { ButtonHTMLAttributes, ReactNode } from "react";
import Link from "next/link";
import { Loader2 } from "lucide-react";

type ButtonVariant = "primary" | "secondary" | "ghost" | "danger";
type ButtonSize = "sm" | "md" | "lg";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  isLoading?: boolean;
  children: ReactNode;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
  asChild?: boolean;
  href?: string;
}

const variantStyles = {
  primary:
    "bg-indigo-600 dark:bg-[#4f51d9] text-white hover:opacity-90 dark:hover:shadow-[0_0_20px_rgba(99,102,241,0.3)] hover:shadow-md active:scale-[0.98] disabled:opacity-60",
  secondary:
    "bg-white dark:bg-[#111216] text-slate-700 dark:text-gray-300 border border-slate-300 dark:border-[#2a2b31] hover:bg-slate-50 dark:hover:bg-[#1a1b20] hover:border-slate-400 dark:hover:border-[#3a3b41] active:bg-slate-100 dark:active:bg-[#25262c] disabled:bg-slate-50 dark:disabled:bg-[#0d0d11] disabled:text-slate-400 dark:disabled:text-gray-500",
  ghost:
    "bg-transparent text-slate-700 dark:text-gray-300 hover:bg-slate-100 dark:hover:bg-[#1a1b20] active:bg-slate-200 dark:active:bg-[#25262c] disabled:text-slate-400 dark:disabled:text-gray-500",
  danger:
    "bg-rose-600 dark:bg-rose-700 text-white hover:bg-rose-700 dark:hover:bg-rose-800 active:bg-rose-800 dark:active:bg-rose-900 disabled:opacity-60",
};

const sizeStyles = {
  sm: "px-3 py-1.5 text-xs",
  md: "px-4 py-2 text-sm",
  lg: "px-5 py-3 text-base",
};

export function Button({
  variant = "primary",
  size = "md",
  isLoading = false,
  children,
  leftIcon,
  rightIcon,
  className = "",
  disabled,
  asChild,
  href,
  type = "button",
  ...props
}: ButtonProps) {
  const baseStyles =
    "inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-all duration-200 cursor-pointer focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 dark:focus:ring-offset-[#0d0d11] disabled:cursor-not-allowed";

  const buttonContent = isLoading ? (
    <span className="flex items-center justify-center gap-2">
      <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
      <span>Loading...</span>
    </span>
  ) : (
    <>
      {leftIcon && <span className="shrink-0" aria-hidden="true">{leftIcon}</span>}
      <span>{children}</span>
      {rightIcon && <span className="shrink-0" aria-hidden="true">{rightIcon}</span>}
    </>
  );

  const buttonClassName = `${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`;

  if (asChild && href) {
    return (
      <Link
        href={href}
        className={buttonClassName}
        aria-disabled={disabled || isLoading}
        aria-busy={isLoading}
      >
        {buttonContent}
      </Link>
    );
  }

  return (
    <button
      type={type}
      className={buttonClassName}
      disabled={disabled || isLoading}
      aria-busy={isLoading}
      {...props}
    >
      {buttonContent}
    </button>
  );
}
