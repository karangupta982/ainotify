"use client";

import { InputHTMLAttributes, TextareaHTMLAttributes, ReactNode } from "react";

interface BaseInputProps {
  label?: string;
  hint?: string;
  error?: string;
  required?: boolean;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
}

interface InputProps
  extends Omit<InputHTMLAttributes<HTMLInputElement>, "size">,
    BaseInputProps {
  as?: "input";
}

interface TextareaProps
  extends Omit<TextareaHTMLAttributes<HTMLTextAreaElement>, "size">,
    BaseInputProps {
  as: "textarea";
}

type FieldProps = InputProps | TextareaProps;

export function Input(props: FieldProps) {
  const {
    label,
    hint,
    error,
    required,
    leftIcon,
    rightIcon,
    className = "",
    id,
    ...inputProps
  } = props;

  const baseInputStyles =
    "w-full h-12 px-4 rounded-lg border bg-white dark:bg-[#111216] text-sm text-slate-900 dark:text-gray-200 shadow-sm transition-colors duration-200 placeholder:text-gray-400 dark:placeholder:text-gray-500 focus:border-indigo-500 dark:focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 dark:focus:ring-indigo-500/30 disabled:bg-slate-50 dark:disabled:bg-[#0d0d11] disabled:text-slate-500 dark:disabled:text-gray-500 disabled:cursor-not-allowed cursor-text";

  const borderStyles = error
    ? "border-rose-300 dark:border-rose-600 focus:border-rose-500 dark:focus:border-rose-500 focus:ring-rose-500/20 dark:focus:ring-rose-500/30"
    : "border-slate-200 dark:border-[#2a2b31] hover:border-slate-300 dark:hover:border-[#3a3b41]";

  const inputClassName = `${baseInputStyles} ${borderStyles} ${className} ${
    leftIcon ? "pl-10" : ""
  } ${rightIcon ? "pr-10" : ""}`;

  const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;
  const hintId = hint ? `${inputId}-hint` : undefined;
  const errorId = error ? `${inputId}-error` : undefined;
  const ariaDescribedBy = [hintId, errorId].filter(Boolean).join(" ") || undefined;

  const inputElement =
    props.as === "textarea" ? (
      <textarea
        id={inputId}
        className={inputClassName}
        aria-invalid={error ? "true" : "false"}
        aria-describedby={ariaDescribedBy}
        {...(inputProps as TextareaHTMLAttributes<HTMLTextAreaElement>)}
      />
    ) : (
      <div className="relative">
        {leftIcon && (
          <div
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 dark:text-gray-500 pointer-events-none"
            aria-hidden="true"
          >
            {leftIcon}
          </div>
        )}
        <input
          id={inputId}
          type={props.type || "text"}
          className={inputClassName}
          aria-invalid={error ? "true" : "false"}
          aria-describedby={ariaDescribedBy}
          {...(inputProps as InputHTMLAttributes<HTMLInputElement>)}
        />
        {rightIcon && (
          <div
            className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 dark:text-gray-500 pointer-events-none"
            aria-hidden="true"
          >
            {rightIcon}
          </div>
        )}
      </div>
    );

  if (!label && !hint && !error) {
    return inputElement;
  }

  return (
    <label
      htmlFor={inputId}
      className="flex flex-col gap-2 text-sm font-medium text-slate-800 dark:text-gray-300"
    >
      {label && (
        <span className="flex items-center gap-1">
          {label}
          {required && (
            <span className="text-rose-500 dark:text-rose-400" aria-label="required">
              *
            </span>
          )}
        </span>
      )}
      {inputElement}
      {hint && !error && (
        <span
          id={hintId}
          className="text-xs font-normal text-slate-500 dark:text-gray-400"
          role="note"
        >
          {hint}
        </span>
      )}
      {error && (
        <span
          id={errorId}
          className="text-xs font-medium text-rose-600 dark:text-rose-400"
          role="alert"
        >
          {error}
        </span>
      )}
    </label>
  );
}
