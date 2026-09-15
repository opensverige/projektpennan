import { useEffect, useRef, useState } from "react"
import { ArrowUpIcon } from "lucide-react"

import { Shell } from "@/components/shell"
import { Button } from "@/components/ui/button"
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from "@/components/ui/input-group"
import { previewTurn } from "@/lib/preview"
import { loadSetup } from "@/lib/setup"

type Msg = { role: "user" | "assistant" | "system"; text: string }

export function ChatPage() {
  const setup = loadSetup()
  const via =
    setup?.auth === "oauth" && setup.provider === "chatgpt"
      ? " med ChatGPT"
      : setup?.auth === "oauth" && setup.provider === "grok"
        ? " med Grok"
        : ""
  const hello = setup?.child
    ? `Hej ${setup.child}. Jag är Gnista${via}. Skriv när det kärvar.`
    : "Hej. Jag är Gnista. Skriv när det kärvar."
  const [messages, setMessages] = useState<Msg[]>([
    { role: "assistant", text: hello },
  ])
  const [draft, setDraft] = useState("")
  const [busy, setBusy] = useState(false)
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [kernel, setKernel] = useState(false)
  const endRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ block: "end" })
  }, [messages, busy])

  async function send() {
    const text = draft.trim()
    if (!text || busy) return
    setDraft("")
    setMessages((m) => [...m, { role: "user", text }])
    setBusy(true)
    try {
      try {
        const response = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session_id: sessionId, message: text }),
        })
        if (response.ok) {
          const data = (await response.json()) as {
            session_id: string
            response: string
            status: string
            mode?: string
          }
          setSessionId(data.session_id)
          if (data.mode === "kernel") setKernel(true)
          setMessages((m) => [...m, { role: "assistant", text: data.response }])
          if (data.status === "error") {
            setMessages((m) => [
              ...m,
              {
                role: "system",
                text: "Något gick fel. Försök igen om du vill.",
              },
            ])
          }
          return
        }
      } catch {
        /* backend sover — samma kärna som test.html */
      }
      const result = await previewTurn(text)
      setKernel(true)
      setSessionId((id) => id || crypto.randomUUID())
      setMessages((m) => [...m, { role: "assistant", text: result.response }])
    } finally {
      setBusy(false)
    }
  }

  return (
    <Shell current="chat">
      <div className="mx-auto flex w-full max-w-2xl flex-1 flex-col px-4">
        {kernel ? (
          <p className="pt-3 text-xs text-muted-foreground">
            Kärnan svarar. Inte Grok. Samma regler som i testet.
          </p>
        ) : null}
        <div className="flex flex-1 flex-col gap-3 overflow-y-auto py-4">
          {messages.map((msg, i) => (
            <div
              key={`${msg.role}-${i}`}
              className={
                msg.role === "user"
                  ? "max-w-[80%] self-end rounded-2xl bg-primary px-4 py-2.5 text-sm text-primary-foreground"
                  : msg.role === "system"
                    ? "self-center rounded-lg bg-muted px-3 py-2 text-xs text-muted-foreground"
                    : "max-w-[80%] self-start rounded-2xl border border-border bg-card px-4 py-2.5 text-sm shadow-xs"
              }
            >
              {msg.text}
            </div>
          ))}
          {busy ? (
            <p className="text-sm text-muted-foreground">Gnista tänker…</p>
          ) : null}
          <div ref={endRef} />
        </div>
        <form
          className="sticky bottom-0 bg-background/80 py-4 backdrop-blur-sm"
          onSubmit={(e) => {
            e.preventDefault()
            void send()
          }}
        >
          <InputGroup className="h-12">
            <InputGroupInput
              value={draft}
              maxLength={1000}
              placeholder="Skriv när det kärvar"
              autoComplete="off"
              onChange={(e) => setDraft(e.target.value)}
            />
            <InputGroupAddon align="inline-end">
              <InputGroupButton
                type="submit"
                size="icon-sm"
                variant="default"
                disabled={busy || !draft.trim()}
                aria-label="Skicka"
              >
                <ArrowUpIcon />
              </InputGroupButton>
            </InputGroupAddon>
          </InputGroup>
          {!setup ? (
            <div className="mt-3 text-center">
              <Button asChild variant="link" size="sm">
                <a href="./start.html">Sätt upp först</a>
              </Button>
            </div>
          ) : null}
        </form>
      </div>
    </Shell>
  )
}
