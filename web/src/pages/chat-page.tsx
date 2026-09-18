import { useEffect, useRef, useState } from "react"
import { ArrowUpIcon, CameraIcon } from "lucide-react"

import { Shell } from "@/components/shell"
import { Button } from "@/components/ui/button"
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from "@/components/ui/input-group"
import { PHOTO_START, firstHook, loadSetup } from "@/lib/setup"

type Msg = {
  role: "user" | "assistant" | "system"
  text: string
  image?: string
}

export function ChatPage() {
  const setup = loadSetup()
  const hello = firstHook(setup)
  const [messages, setMessages] = useState<Msg[]>([
    { role: "assistant", text: hello },
  ])
  const [draft, setDraft] = useState("")
  const [busy, setBusy] = useState(false)
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [kernel, setKernel] = useState(false)
  const [soulModel, setSoulModel] = useState<string | null>(null)
  const endRef = useRef<HTMLDivElement>(null)
  const fileRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ block: "end" })
  }, [messages, busy])

  async function send(text: string, image?: string) {
    const payload = text.trim() || (image ? PHOTO_START : "")
    if (!payload || busy) return
    setDraft("")
    setMessages((m) => [...m, { role: "user", text: payload, image }])
    setBusy(true)
    try {
      try {
        const key =
          typeof sessionStorage !== "undefined"
            ? sessionStorage.getItem("utter-key")
            : null
        const headers: Record<string, string> = {
          "Content-Type": "application/json",
        }
        if (key) headers["X-Utter-Key"] = key
        if (setup?.provider) headers["X-Utter-Provider"] = setup.provider
        const response = await fetch("/api/chat", {
          method: "POST",
          headers,
          body: JSON.stringify({ session_id: sessionId, message: payload }),
        })
        if (response.ok) {
          const data = (await response.json()) as {
            session_id: string
            response: string
            status: string
            mode?: string
            model?: string
          }
          setSessionId(data.session_id)
          if (data.mode === "kernel") setKernel(true)
          if (data.mode === "soul") {
            setKernel(false)
            setSoulModel(data.model || "SOUL")
          }
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
        /* backend sover */
      }
      setMessages((m) => [
        ...m,
        {
          role: "system",
          text: "Ingen modell. Klistra en nyckel på startsidan eller sätt OPENAI_API_KEY / GROQ_API_KEY hemma.",
        },
      ])
    } finally {
      setBusy(false)
    }
  }

  function onPhoto(file: File | undefined) {
    if (!file || busy) return
    const url = URL.createObjectURL(file)
    void send(PHOTO_START, url)
  }

  return (
    <Shell current="chat">
      <div className="mx-auto flex w-full max-w-2xl flex-1 flex-col px-4">
        {soulModel ? (
          <p className="pt-3 text-xs text-muted-foreground">
            SOUL + {soulModel}. Modellen undervisar. Koden stoppar det farliga.
          </p>
        ) : kernel ? (
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
                  ? "max-w-[80%] self-end overflow-hidden rounded-2xl bg-primary text-sm text-primary-foreground"
                  : msg.role === "system"
                    ? "self-center rounded-lg bg-muted px-3 py-2 text-xs text-muted-foreground"
                    : "max-w-[80%] self-start rounded-2xl border border-border bg-card px-4 py-2.5 text-sm shadow-xs"
              }
            >
              {msg.image ? (
                <img
                  src={msg.image}
                  alt=""
                  className="max-h-64 w-full object-cover"
                />
              ) : null}
              <p className={msg.role === "user" ? "px-4 py-2.5" : undefined}>
                {msg.text}
              </p>
            </div>
          ))}
          {busy ? (
            <p className="text-sm text-muted-foreground">Utter tänker…</p>
          ) : null}
          <div ref={endRef} />
        </div>
        <form
          className="sticky bottom-0 bg-background/80 py-4 backdrop-blur-sm"
          onSubmit={(e) => {
            e.preventDefault()
            void send(draft)
          }}
        >
          <input
            ref={fileRef}
            type="file"
            accept="image/*"
            capture="environment"
            className="sr-only"
            tabIndex={-1}
            onChange={(e) => {
              onPhoto(e.target.files?.[0])
              e.target.value = ""
            }}
          />
          <InputGroup className="h-12">
            <InputGroupAddon align="inline-start">
              <InputGroupButton
                type="button"
                size="icon-sm"
                aria-label="Skicka bilden"
                disabled={busy}
                onClick={() => fileRef.current?.click()}
              >
                <CameraIcon />
              </InputGroupButton>
            </InputGroupAddon>
            <InputGroupInput
              value={draft}
              maxLength={1000}
              placeholder="Eller skriv när det kärvar"
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
