"use client";

import * as React from "react";

export interface AvatarProps
  extends React.HTMLAttributes<HTMLDivElement> {
  initials?: string;
}

export const Avatar = React.forwardRef<HTMLDivElement, AvatarProps>(
  ({ className = "", initials, children, ...props }, ref) => {
    const classes = [
      "flex h-8 w-8 items-center justify-center rounded-full bg-zinc-100 text-xs font-medium text-zinc-700",
      className,
    ]
      .filter(Boolean)
      .join(" ");

    return (
      <div ref={ref} className={classes} {...props}>
        {initials ?? children}
      </div>
    );
  },
);

Avatar.displayName = "Avatar";

