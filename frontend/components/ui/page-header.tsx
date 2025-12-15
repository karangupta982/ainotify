import { ReactNode } from "react";

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  badge?: string;
  actions?: ReactNode;
  className?: string;
}

export function PageHeader({
  title,
  subtitle,
  badge,
  actions,
  className = "",
}: PageHeaderProps) {
  return (
    <div className={`flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between ${className}`}>
      <div className="flex-1">
        <div className="flex items-center gap-3">
          {badge && (
            <span className="text-xs font-semibold uppercase tracking-wide text-indigo-600 dark:text-indigo-400">
              {badge}
            </span>
          )}
        </div>
        <h1 className="text-4xl font-semibold text-slate-900 dark:text-white leading-tight mt-2">
          {title}
        </h1>
        {subtitle && (
          <p className="text-base text-gray-600 dark:text-gray-300 leading-relaxed mt-2">
            {subtitle}
          </p>
        )}
      </div>
      {actions && <div className="flex items-center gap-2 mt-4 sm:mt-0">{actions}</div>}
    </div>
  );
}

