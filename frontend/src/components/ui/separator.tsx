"use client";

import * as React from "react";

export interface SeparatorProps
  extends React.HTMLAttributes<HTMLDivElement> {
  orientation?: "horizontal" | "vertical";
}

export const Separator = React.forwardRef<HTMLDivElement, SeparatorProps>(
  ({ className = "", orientation = "horizontal", ...props }, ref) => {
    const base =
      "bg-zinc-200 dark:bg-zinc-800 shrink-0";
    const orientationClass =
      orientation === "vertical" ? "w-px h-full" : "h-px w-full";

    const classes = [base, orientationClass, className]
      .filter(Boolean)
      .join(" ");

    return <div ref={ref} className={classes} {...props} />;
  },
);

Separator.displayName = "Separator";

