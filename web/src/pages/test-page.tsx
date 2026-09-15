import { useMemo, useRef, useState } from "react"
import { ArrowUpIcon } from "lucide-react"

import { Shell } from "@/components/shell"
import { Button } from "@/components/ui/button"
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
  const [messages, setMessages] = useState<Msg[]>([
    {
      role: "assistant",
      text: `Hej. Jag är Gnista. Tryck ett chip så ser du hur jag möter ${child}.`,
    },
  ])
  const endRef = useRef<HTMLDivElement>(null)

  const chips = useMemo(() => SCENARIOS, [])

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
              Se hur Gnista möter {child}
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
