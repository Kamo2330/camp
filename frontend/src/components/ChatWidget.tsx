'use client';

import { FormEvent, useEffect, useRef, useState } from 'react';
import { sendChatMessage } from '@/lib/api';

type ChatMessage = {
  id: string;
  role: 'user' | 'assistant';
  text: string;
  mode?: string;
};

const STARTERS = [
  'What services do you offer?',
  'How do I get a quote?',
  'How can I contact you?',
];

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      role: 'assistant',
      text: 'Hi — I am the Camp Security assistant. Ask about services, quotes, careers, or contact details.',
    },
  ]);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, open]);

  async function ask(question: string) {
    const trimmed = question.trim();
    if (!trimmed || loading) return;

    const userMsg: ChatMessage = {
      id: `u-${Date.now()}`,
      role: 'user',
      text: trimmed,
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const { reply, mode } = await sendChatMessage(trimmed);
      setMessages((prev) => [
        ...prev,
        { id: `a-${Date.now()}`, role: 'assistant', text: reply, mode },
      ]);
    } catch (err) {
      const message =
        err instanceof Error ? err.message : 'Could not reach the assistant.';
      setMessages((prev) => [
        ...prev,
        {
          id: `e-${Date.now()}`,
          role: 'assistant',
          text: `${message} You can still use the Contact page.`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function onSubmit(e: FormEvent) {
    e.preventDefault();
    void ask(input);
  }

  return (
    <div className="fixed bottom-5 right-5 z-50 flex flex-col items-end gap-3">
      {open && (
        <div className="flex h-[min(520px,70vh)] w-[min(380px,calc(100vw-2rem))] flex-col overflow-hidden rounded-2xl border border-soft-border bg-surface shadow-card">
          <div className="flex items-center justify-between border-b border-soft-border bg-surface-2 px-4 py-3">
            <div>
              <p className="text-sm font-semibold text-text">Camp Assistant</p>
              <p className="text-xs text-muted">AI chatbot · services &amp; contact help</p>
            </div>
            <button
              type="button"
              onClick={() => setOpen(false)}
              className="rounded-lg px-2 py-1 text-sm text-muted hover:bg-soft-border hover:text-text"
              aria-label="Close chat"
            >
              ✕
            </button>
          </div>

          <div className="flex-1 space-y-3 overflow-y-auto px-3 py-3">
            {messages.map((m) => (
              <div
                key={m.id}
                className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[85%] whitespace-pre-wrap rounded-2xl px-3 py-2 text-sm leading-relaxed ${
                    m.role === 'user'
                      ? 'bg-accent text-white'
                      : 'border border-soft-border bg-surface-2 text-text'
                  }`}
                >
                  {m.text}
                  {m.role === 'assistant' && m.mode && (
                    <p className="mt-1 text-[10px] uppercase tracking-wide text-muted">
                      {m.mode === 'llm' ? 'AI reply' : 'FAQ reply'}
                    </p>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <p className="text-xs text-muted px-1">Assistant is typing…</p>
            )}
            <div ref={bottomRef} />
          </div>

          <div className="flex flex-wrap gap-2 border-t border-soft-border px-3 py-2">
            {STARTERS.map((s) => (
              <button
                key={s}
                type="button"
                disabled={loading}
                onClick={() => void ask(s)}
                className="rounded-full border border-soft-border px-2.5 py-1 text-[11px] text-muted hover:border-accent hover:text-text disabled:opacity-50"
              >
                {s}
              </button>
            ))}
          </div>

          <form onSubmit={onSubmit} className="flex gap-2 border-t border-soft-border p-3">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about services, quotes…"
              className="flex-1 rounded-xl border border-soft-border bg-bg px-3 py-2 text-sm text-text outline-none focus:border-accent"
              disabled={loading}
            />
            <button type="submit" className="btn !px-3 !py-2 text-sm" disabled={loading}>
              Send
            </button>
          </form>
        </div>
      )}

      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="btn !rounded-full !px-5 !py-3 text-sm font-semibold shadow-btn"
        aria-expanded={open}
      >
        {open ? 'Close chat' : 'Chat with us'}
      </button>
    </div>
  );
}
