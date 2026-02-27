"use client";

import { useState } from "react";

import { Avatar } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Textarea } from "@/components/ui/textarea";

type Role = "user" | "assistant";

interface Message {
  id: string;
  role: Role;
  content: string;
  action?: string;
  toolName?: string | null;
  isClarifying?: boolean;
}

const INITIAL_MESSAGES: Message[] = [
  {
    id: "m-0",
    role: "assistant",
    content:
      "Hello, this is Bookly Support. How may I assist you with your order or account today?",
    action: "answer",
    toolName: null,
    isClarifying: false,
  },
];

export default function Home() {
  const [messages, setMessages] = useState<Message[]>(INITIAL_MESSAGES);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);

  async function handleSend() {
    const trimmed = input.trim();
    if (!trimmed || isSending) return;

    const userMessage: Message = {
      id: `m-${Date.now()}`,
      role: "user",
      content: trimmed,
    };

    const nextMessages = [...messages, userMessage];
    setMessages(nextMessages);
    setInput("");
    setIsSending(true);

    try {
      const payload = {
        conversation_id: "web-session",
        messages: nextMessages.map((m) => ({
          role: m.role,
          content: m.content,
        })),
      };

      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      const assistant = data.message as { role: Role; content: string };
      const meta = data.action_metadata as {
        action: string;
        tool_name?: string | null;
        is_clarifying_question?: boolean;
      };

      const assistantMessage: Message = {
        id: `m-${Date.now()}-assistant`,
        role: "assistant",
        content: assistant.content,
        action: meta.action,
        toolName: meta.tool_name,
        isClarifying: meta.is_clarifying_question,
      };

      setMessages((current) => [...current, assistantMessage]);
    } catch {
      const assistantMessage: Message = {
        id: `m-${Date.now()}-error`,
        role: "assistant",
        content:
          "I was unable to reach the Bookly support service. Please try again in a moment.",
        action: "error",
        toolName: null,
        isClarifying: false,
      };
      setMessages((current) => [...current, assistantMessage]);
    } finally {
      setIsSending(false);
    }
  }

  function handleKeyDown(event: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-100 px-4 py-6 text-zinc-900">
      <div className="flex w-full max-w-6xl gap-4">
        <aside className="hidden w-64 flex-col rounded-xl border border-zinc-200 bg-white/90 p-4 shadow-sm sm:flex">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                Workspace
              </p>
              <p className="text-sm font-medium text-zinc-900">
                Bookly Support
              </p>
            </div>
            <Badge variant="outline">Agent</Badge>
          </div>
          <Separator className="my-2" />
          <div className="mb-2 flex items-center justify-between">
            <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
              Conversations
            </p>
            <Badge variant="default">Live</Badge>
          </div>
          <div className="mt-2 space-y-2">
            <div className="rounded-lg border border-zinc-200 bg-zinc-50 px-3 py-2">
              <p className="text-xs font-medium text-zinc-900">
                Current session
              </p>
              <p className="text-xs text-zinc-500">
                Synthetic Bookly customer demo
              </p>
            </div>
            <div className="rounded-lg border border-dashed border-zinc-200 px-3 py-2">
              <p className="text-xs text-zinc-500">
                Additional conversations would appear here in a real console.
              </p>
            </div>
          </div>
        </aside>

        <Card className="flex flex-1 flex-col overflow-hidden rounded-2xl border-zinc-200 bg-white/95 shadow-md">
          <CardHeader className="flex items-center justify-between border-b border-zinc-200 bg-zinc-50/80">
            <div className="flex items-center gap-3">
              <div className="flex h-8 w-20 items-center justify-between rounded-full bg-zinc-200/70 px-2">
                <span className="h-2 w-2 rounded-full bg-red-400" />
                <span className="h-2 w-2 rounded-full bg-amber-300" />
                <span className="h-2 w-2 rounded-full bg-emerald-400" />
              </div>
              <div>
                <CardTitle>Bookly Support Console</CardTitle>
                <CardDescription>
                  Formal, concise AI agent for order and account help.
                </CardDescription>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Badge variant="outline">Online</Badge>
              <Avatar initials="BS" />
            </div>
          </CardHeader>

          <CardContent className="flex flex-1 flex-col gap-4 bg-white/80 p-0">
            <div className="flex items-center justify-between border-b border-zinc-200 px-4 py-2 text-xs text-zinc-500">
              <span>Session: web-session</span>
              <span>
                Messages:{" "}
                <span className="font-medium text-zinc-700">
                  {messages.length}
                </span>
              </span>
            </div>

            <ScrollArea className="flex-1 px-4 pb-4 pt-2">
              <div className="flex flex-col gap-3">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex items-start gap-3 ${
                      message.role === "user"
                        ? "justify-end text-right"
                        : "justify-start text-left"
                    }`}
                  >
                    {message.role === "assistant" && (
                      <Avatar initials="A" className="mt-1 shrink-0" />
                    )}
                    <div
                      className={`max-w-xl rounded-2xl px-3 py-2 text-sm ${
                        message.role === "user"
                          ? "bg-zinc-900 text-zinc-50"
                          : "bg-zinc-100 text-zinc-900"
                      }`}
                    >
                      <p className="whitespace-pre-wrap">{message.content}</p>
                      <div className="mt-1 flex flex-wrap gap-1 text-[10px] text-zinc-500">
                        {message.action === "call_tool" && message.toolName && (
                          <Badge variant="outline">
                            Tool: {message.toolName}
                          </Badge>
                        )}
                        {message.isClarifying && (
                          <Badge variant="outline">Clarification</Badge>
                        )}
                        {message.action === "error" && (
                          <Badge variant="outline">Error</Badge>
                        )}
                      </div>
                    </div>
                    {message.role === "user" && (
                      <Avatar initials="U" className="mt-1 shrink-0" />
                    )}
                  </div>
                ))}
              </div>
            </ScrollArea>
          </CardContent>

          <CardFooter className="border-t border-zinc-200 bg-zinc-50/80">
            <div className="flex w-full flex-col gap-2">
              <Textarea
                value={input}
                onChange={(event) => setInput(event.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type a customer message, for example: “Where is my order B-1002?”"
                rows={3}
              />
              <div className="flex items-center justify-between gap-2">
                <div className="flex flex-wrap gap-2 text-[11px] text-zinc-500">
                  <span>Press Enter to send</span>
                  <span className="text-zinc-400">•</span>
                  <span>Shift+Enter for a new line</span>
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    disabled={isSending}
                    onClick={() => {
                      setInput(
                        "I would like to return the book from order B-1001. It arrived damaged.",
                      );
                    }}
                  >
                    Sample refund flow
                  </Button>
                  <Button
                    type="button"
                    size="md"
                    onClick={handleSend}
                    disabled={isSending || !input.trim()}
                  >
                    {isSending ? "Sending..." : "Send"}
                  </Button>
                </div>
              </div>
            </div>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}

