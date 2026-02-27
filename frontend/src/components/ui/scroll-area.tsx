"use client";

import * as React from "react";

export type ScrollAreaProps = React.HTMLAttributes<HTMLDivElement>;

export const ScrollArea = React.forwardRef<HTMLDivElement, ScrollAreaProps>(
  ({ className = "", children, ...props }, ref) => {
    const classes = [
      "relative overflow-y-auto scrollbar-thin scrollbar-track-transparent scrollbar-thumb-zinc-300",
      className,
    ]
      .filter(Boolean)
      .join(" ");

    return (
      <div ref={ref} className={classes} {...props}>
        {children}
      </div>
    );
  },
);

ScrollArea.displayName = "ScrollArea";

