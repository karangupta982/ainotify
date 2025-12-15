// Legacy Field component - use Input component instead
// Kept for backward compatibility
"use client";

import { Input } from "./input";

type FieldProps = {
  label: string;
  hint?: string;
  id: string;
  type?: string;
  value: string;
  onChange: (v: string) => void;
  required?: boolean;
};

export function Field({
  label,
  hint,
  id,
  type = "text",
  value,
  onChange,
  required,
}: FieldProps) {
  return (
    <Input
      id={id}
      type={type}
      label={label}
      hint={hint}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      required={required}
    />
  );
}
