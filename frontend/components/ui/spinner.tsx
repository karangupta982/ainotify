import { Loader2 } from "lucide-react";

interface SpinnerProps {
  size?: "sm" | "md" | "lg";
  className?: string;
  centered?: boolean;
  text?: string;
}

const sizeStyles = {
  sm: "h-4 w-4",
  md: "h-6 w-6",
  lg: "h-8 w-8",
};

export function Spinner({
  size = "md",
  className = "",
  centered = false,
  text,
}: SpinnerProps) {
  const spinner = (
    <Loader2
      className={`${sizeStyles[size]} animate-spin text-indigo-600 dark:text-indigo-400 ${className}`}
      role="status"
      aria-label="Loading"
    />
  );

  if (centered) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[200px] gap-3">
        {spinner}
        {text && (
          <p className="text-sm text-slate-600 dark:text-gray-400">{text}</p>
        )}
      </div>
    );
  }

  if (text) {
    return (
      <div className="flex items-center gap-2">
        {spinner}
        <span className="text-sm text-slate-600 dark:text-gray-400">{text}</span>
      </div>
    );
  }

  return spinner;
}
