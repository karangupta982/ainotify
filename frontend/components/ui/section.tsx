import { ReactNode, HTMLAttributes } from "react";

interface SectionProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
  title?: string;
  description?: string;
  spacing?: "sm" | "md" | "lg";
}

const spacingStyles = {
  sm: "space-y-3",
  md: "space-y-6",
  lg: "space-y-8",
};

export function Section({
  children,
  title,
  description,
  spacing = "md",
  className = "",
  ...props
}: SectionProps) {
  return (
    <section
      className={`mx-auto max-w-7xl px-6 md:px-12 lg:px-24 ${spacingStyles[spacing]} ${className}`}
      {...props}
    >
      {title && (
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-semibold text-slate-900 dark:text-white leading-tight mb-4">
            {title}
          </h2>
          {description && (
            <p className="text-base text-gray-600 dark:text-gray-300 leading-relaxed max-w-2xl mx-auto">
              {description}
            </p>
          )}
        </div>
      )}
      {children}
    </section>
  );
}

