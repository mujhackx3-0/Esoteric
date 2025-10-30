"use client";
import { useEffect, useRef, useState } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function LuChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const endRef = useRef<HTMLDivElement | null>(null);

  // 1. Create a backend session on load
  useEffect(() => {
    (async () => {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/v1/sessions`, {
        method: "POST",
      });
      const data = await res.json();
      setSessionId(data.session_id);
    })();
  }, []);

  // 2. Open WebSocket once we have sessionId
  useEffect(() => {
    if (!sessionId) return;
    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";
    const ws = new WebSocket(`${wsUrl}/api/v1/ws/${sessionId}`);
    wsRef.current = ws;

    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.type === "message")
        setMessages((m) => [...m, { role: "assistant", content: data.content }]);
    };

    return () => ws.close();
  }, [sessionId]);

  // 3. Auto-scroll
  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // 4. Send a message
  const sendMessage = () => {
    if (!input.trim()) return;
    setMessages((m) => [...m, { role: "user", content: input }]);
    wsRef.current?.send(JSON.stringify({ message: input }));
    setInput("");
  };

  return (
    <div className="flex flex-col h-screen bg-[#0D1117] text-[#E6EDF3]">
      {/* Header */}
      <header className="px-6 py-4 border-b border-[#21262D] bg-[#161B22] text-xl font-semibold">
        Lu — Loan Sales Assistant 🤖
      </header>

      {/* Messages */}
      <main className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`max-w-xl px-4 py-2 rounded-2xl break-words ${
              msg.role === "user"
                ? "bg-[#30363D] self-end ml-auto"
                : "bg-[#1F6FEB] text-white self-start"
            }`}
          >
            {msg.content}
          </div>
        ))}
        <div ref={endRef} />
      </main>

      {/* Input */}
      <footer className="border-t border-[#21262D] bg-[#161B22] p-4 flex gap-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Ask Lu something..."
          className="flex-1 bg-[#1E2630] text-[#E6EDF3] rounded-lg px-4 py-2 focus:outline-none"
        />
        <button
          onClick={sendMessage}
          className="bg-[#1F6FEB] hover:bg-[#388BFD] px-4 py-2 rounded-lg text-white"
        >
          Send
        </button>
      </footer>
    </div>
  );
}
