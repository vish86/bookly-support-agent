"use client";

import * as React from "react";

export const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className = "", ...props }, ref) => {
  const classes = [
    "rounded-xl border border-zinc-200 bg-white text-zinc-950 shadow-sm",
    className,
  ]
    .filter(Boolean)
    .join(" ");

  return <div ref={ref} className={classes} {...props} />;
});

Card.displayName = "Card";

export const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className = "", ...props }, ref) => {
  const classes = ["flex flex-col space-y-1.5 p-4", className]
    .filter(Boolean)
    .join(" ");
  return <div ref={ref} className={classes} {...props} />;
});

CardHeader.displayName = "CardHeader";

export const CardTitle = React.forwardRef<
  HTMLHeadingElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className = "", ...props }, ref) => {
  const classes = [
    "text-sm font-semibold leading-none tracking-tight",
    className,
  ]
    .filter(Boolean)
    .join(" ");
  return <h2 ref={ref} className={classes} {...props} />;
});

CardTitle.displayName = "CardTitle";

export const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className = "", ...props }, ref) => {
  const classes = ["text-xs text-zinc-500", className]
    .filter(Boolean)
    .join(" ");
  return <p ref={ref} className={classes} {...props} />;
});

CardDescription.displayName = "CardDescription";

export const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className = "", ...props }, ref) => {
  const classes = ["p-4 pt-0", className].filter(Boolean).join(" ");
  return <div ref={ref} className={classes} {...props} />;
});

CardContent.displayName = "CardContent";

export const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className = "", ...props }, ref) => {
  const classes = ["flex items-center p-4 pt-0", className]
    .filter(Boolean)
    .join(" ");
  return <div ref={ref} className={classes} {...props} />;
});

CardFooter.displayName = "CardFooter";

