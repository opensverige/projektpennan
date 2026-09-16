import { useEffect, useMemo, useRef, useState } from "react"
import { ArrowUpIcon } from "lucide-react"
import { toast } from "sonner"

import { Shell } from "@/components/shell"
import { Button } from "@/components/ui/button"
import { Field, FieldDescription, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from "@/components/ui/input-group"
import { PLAN, SCENARIOS, previewTurn } from "@/lib/preview"
import { loadSetup } from "@/lib/setup"
import { bindTelegram, telegramStatus, type TelegramStatus } from "@/lib/telegram"
import { cn } from "@/lib/utils"

type Msg = { role: "user" | "assistant"; text: string }

function goChat() {
  window.location.href = "./index.html"
}

export function TestPage() {
  const setup = loadSetup()
  const child = setup?.child || "barnet"
  const [hit, setHit] = useState<string>("socratic")
  const [draft, setDraft] = useState("")
  const [busy, setBusy] = useState(false)
  const [tg, setTg] = useState<TelegramStatus>({})
  const [messages, setMessages] = useState<Msg[]>([
    {
      role: "assistant",
      text: `Hej. Jag är Utter. Tryck ett chip så ser du hur jag möter ${child}.`,
    },
  ])
  const endRef = useRef<HTMLDivElement>(null)

  const chips = useMemo(() => SCENARIOS, [])

  useEffect(() => {
    void telegramStatus().then(setTg)
  }, [])

  async function play(text: string) {
    const message = text.trim()
    if (!message || busy) return
    setDraft("")
    setBusy(true)
    setMessages((m) => [...m, { role: "user", text: message }])
    const result = await previewTurn(message)
    setHit(result.plan_hit)
    setMessages((m) => [...m, { role: "assistant", text: result.response }])
    setBusy(false)
    queueMicrotask(() => endRef.current?.scrollIntoView({ block: "end" }))
  }

  return (
    <Shell current="test">
      <section className="mx-auto flex w-full max-w-5xl flex-1 flex-col gap-8 px-4 pb-10 pt-2 md:flex-row md:items-start">
        <div className="flex flex-1 flex-col gap-5">
          <div>
            <p className="text-sm text-muted-foreground">Testmiljö — du är föräldern</p>
            <h1 className="font-heading text-3xl font-semibold tracking-tight">
              Se hur Utter möter {child}
            </h1>
            <p className="mt-2 text-sm text-muted-foreground">
              Planen sitter i koden. Tryck ett chip, även de opassande.
              Så vet du vad som händer innan {child} gör det.
            </p>
          </div>

          <ul className="grid gap-2">
            {PLAN.map((item) => (
              <li
                key={item.id}
                className={cn(
                  "rounded-xl border px-4 py-3",
                  hit === item.id
                    ? "border-primary bg-primary/5"
                    : "border-border bg-card"
                )}
              >
                <p className="text-sm font-medium">{item.title}</p>
                <p className="text-sm text-muted-foreground">{item.text}</p>
              </li>
            ))}
          </ul>

          <div className="flex flex-wrap gap-2">
            {chips.map((scene) => (
              <Button
                key={scene.id}
                type="button"
                size="sm"
                variant={scene.kind === "socratic" || scene.kind === "answer" ? "outline" : "secondary"}
                className="rounded-full"
                disabled={busy}
                onClick={() => void play(scene.child)}
              >
                {scene.chip}
              </Button>
            ))}
          </div>

          <TelegramLink child={child} status={tg} onBound={setTg} />
        </div>

        <Card className="w-full md:max-w-sm md:sticky md:top-4">
          <CardHeader className="border-b">
            <CardTitle>Som {child} ser det</CardTitle>
            <CardDescription>
              Inget lämnar den här skärmen. Backend sover? Kärnan kör ändå.
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            <div className="flex max-h-[28rem] min-h-64 flex-col gap-2 overflow-y-auto py-1">
              {messages.map((msg, i) => (
                <div
                  key={`${msg.role}-${i}`}
                  className={
                    msg.role === "user"
                      ? "max-w-[85%] self-end rounded-2xl bg-primary px-3 py-2 text-sm text-primary-foreground"
                      : "max-w-[90%] self-start rounded-2xl border border-border bg-background px-3 py-2 text-sm"
                  }
                >
                  {msg.text}
                </div>
              ))}
              <div ref={endRef} />
            </div>
            <form
              onSubmit={(e) => {
                e.preventDefault()
                void play(draft)
              }}
            >
              <InputGroup className="h-11">
                <InputGroupInput
                  value={draft}
                  placeholder="Eller skriv som barnet"
                  autoComplete="off"
                  onChange={(e) => setDraft(e.target.value)}
                />
                <InputGroupAddon align="inline-end">
                  <InputGroupButton
                    type="submit"
                    size="icon-sm"
                    variant="default"
                    disabled={busy || !draft.trim()}
                    aria-label="Skicka test"
                  >
                    <ArrowUpIcon />
                  </InputGroupButton>
                </InputGroupAddon>
              </InputGroup>
            </form>
            <Button type="button" onClick={goChat}>
              Ser tryggt ut — släpp in {child}
            </Button>
            <Button type="button" variant="link" className="h-auto p-0" onClick={goChat}>
              Hoppa över
            </Button>
          </CardContent>
        </Card>
      </section>
    </Shell>
  )
}

function TelegramLink({
  child,
  status,
  onBound,
}: {
  child: string
  status: TelegramStatus
  onBound: (s: TelegramStatus) => void
}) {
  const [token, setToken] = useState("")
  const [busy, setBusy] = useState(false)

  async function bind() {
    if (!token.trim()) return
    setBusy(true)
    const result = await bindTelegram(token.trim())
    setBusy(false)
    if (result.detail) {
      toast(result.detail)
      return
    }
    setToken("")
    onBound(result)
    if (result.invite) {
      await navigator.clipboard.writeText(result.invite)
      toast("Länken är kopierad. Öppna den i din Telegram.")
    }
  }

  return (
    <div className="rounded-xl border border-border bg-card px-4 py-4">
      <p className="text-sm font-medium">{child} skriver i Telegram</p>
      <p className="mt-1 text-sm text-muted-foreground">
        Inte vår bot. Du skapar en hos BotFather. Tokenen stannar här.
        Ingen verifier-bot som tar emot nyckeln.
      </p>
      <div className="mt-3 flex flex-col gap-2">
        <Button asChild variant="outline" size="sm">
          <a href="https://t.me/BotFather" target="_blank" rel="noreferrer">
            Öppna @BotFather
          </a>
        </Button>
        <Field>
          <FieldLabel htmlFor="tg-token">Klistra token</FieldLabel>
          <Input
            id="tg-token"
            type="password"
            value={token}
            autoComplete="off"
            placeholder="123456:AA…"
            onChange={(e) => setToken(e.target.value)}
          />
          <FieldDescription>
            /newbot hos dem. Sen klistra här. Vi kör getMe lokalt.
          </FieldDescription>
        </Field>
        <Button type="button" size="sm" disabled={busy || !token.trim()} onClick={() => void bind()}>
          Skapa start-länk
        </Button>
        {status.invite ? (
          <p className="break-all text-sm">
            <a href={status.invite} className="underline underline-offset-4" target="_blank" rel="noreferrer">
              {status.invite}
            </a>
            {status.linked ? " — länkad." : " — öppna den, sen kan barnet skriva."}
          </p>
        ) : null}
      </div>
    </div>
  )
}
