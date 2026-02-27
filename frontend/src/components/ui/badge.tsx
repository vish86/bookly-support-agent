"use client";

import * as React from "react";

type BadgeVariant = "default" | "outline";

const baseClasses =
  "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium";

const variantClasses: Record<BadgeVariant, string> = {
  default: "border-transparent bg-zinc-900 text-zinc-50",
  outline: "border-zinc-200 text-zinc-600",
};

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant;
}

export const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  ({ className = "", variant = "default", ...props }, ref) => {
    const classes = [baseClasses, variantClasses[variant], className]
      .filter(Boolean)
      .join(" ");

    return <span ref={ref} className={classes} {...props} />;
  },
);

Badge.displayName = "Badge";

