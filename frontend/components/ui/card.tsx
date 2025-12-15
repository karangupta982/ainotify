import { ReactNode, HTMLAttributes } from "react";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
  hover?: boolean;
  padding?: "none" | "sm" | "md" | "lg";
}

const paddingStyles = {
  none: "",
  sm: "p-3",
  md: "p-6",
  lg: "p-8",
};

export function Card({
  children,
  hover = false,
  padding = "md",
  className = "",
  ...props
}: CardProps) {
  const baseStyles =
    "rounded-xl border border-slate-200 dark:border-[#2a2b31] bg-white dark:bg-[#111216] shadow-sm dark:shadow-none transition-all duration-200";

  const hoverStyles = hover
    ? "hover:shadow-md dark:hover:shadow-[0_0_20px_rgba(99,102,241,0.1)] hover:-translate-y-0.5"
    : "";

  return (
    <div
      className={`${baseStyles} ${hoverStyles} ${paddingStyles[padding]} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
