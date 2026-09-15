import { useMemo, useState } from "react"
import { ArrowUpIcon, EyeIcon, EyeOffIcon } from "lucide-react"
import { toast } from "sonner"

import Aurora from "@/components/Aurora"
import { Shell } from "@/components/shell"
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field"
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from "@/components/ui/input-group"
import { Input } from "@/components/ui/input"
import { DOCKER, PROMPT, providerLabel, saveSetup } from "@/lib/setup"

function goChat() {
  window.location.href = "./index.html"
}

export function StartPage() {
  const [name, setName] = useState("")
  const [key, setKey] = useState("")
  const [consent, setConsent] = useState(false)
  const [showKey, setShowKey] = useState(false)
  const [hint, setHint] = useState(false)
  const reduceMotion = useMemo(
    () => window.matchMedia("(prefers-reduced-motion: reduce)").matches,
    []
  )

  const child = name.trim().split(/\s+/)[0] || ""
  const ready = consent && child.length >= 2
  const label = providerLabel(key)

  function submit(skipKey: boolean) {
    if (!ready) {
      setHint(true)
      return
    }
    saveSetup(child, skipKey ? "" : key.trim())
    goChat()
  }

  return (
    <Shell current="start">
      <section className="relative flex flex-1 flex-col items-center justify-center px-4 pb-10">
        {!reduceMotion ? (
          <div className="pointer-events-none absolute inset-0 -z-10 overflow-hidden">
            <Aurora
              lightMode
              amplitude={0.85}
              blend={0.55}
              speed={0.35}
              colorStops={["#c4b5a0", "#9aa4b2", "#a8c3b5"]}
            />
          </div>
        ) : (
          <div className="absolute inset-0 -z-10 bg-muted" />
        )}

        <div className="flex w-full max-w-sm flex-col items-center gap-6">
          <div className="text-center">
            <p className="text-sm text-muted-foreground">Föräldern slår på den</p>
            <h1 className="font-heading text-3xl font-semibold tracking-tight">
              Gnista
            </h1>
          </div>

          <form
            className="flex w-full flex-col gap-5 rounded-xl border border-border bg-background/90 px-6 py-7 shadow-md backdrop-blur-sm"
            autoComplete="off"
            onSubmit={(e) => {
              e.preventDefault()
              submit(false)
            }}
          >
            <FieldGroup>
              <Field data-invalid={hint && child.length < 2}>
                <FieldLabel htmlFor="name">Vad heter barnet?</FieldLabel>
                <Input
                  id="name"
                  value={name}
                  maxLength={40}
                  placeholder="Alma"
                  aria-invalid={hint && child.length < 2}
                  onChange={(e) => setName(e.target.value)}
                />
              </Field>

              <Field>
                <FieldLabel htmlFor="key">Nyckel</FieldLabel>
                <InputGroup className="h-11">
                  <InputGroupInput
                    id="key"
                    type={showKey ? "text" : "password"}
                    value={key}
                    placeholder="Klistra in nyckeln här"
                    autoComplete="off"
                    onChange={(e) => setKey(e.target.value)}
                  />
                  <InputGroupAddon align="inline-end">
                    <InputGroupButton
                      size="icon-sm"
                      aria-label={showKey ? "Dölj nyckel" : "Visa nyckel"}
                      onClick={() => setShowKey((v) => !v)}
                    >
                      {showKey ? <EyeOffIcon /> : <EyeIcon />}
                    </InputGroupButton>
                    <InputGroupButton
                      type="submit"
                      size="icon-sm"
                      variant="default"
                      disabled={!ready}
                      aria-label="Sätt igång"
                    >
                      <ArrowUpIcon />
                    </InputGroupButton>
                  </InputGroupAddon>
                </InputGroup>
                {label ? (
                  <Badge variant="secondary">Det där ser ut som {label}</Badge>
                ) : (
                  <FieldDescription>
                    Valfritt. Har du en nyckel från ChatGPT, Claude eller Gemini —
                    klistra in den.
                  </FieldDescription>
                )}
              </Field>

              <Field orientation="horizontal" data-invalid={hint && !consent}>
                <Checkbox
                  id="consent"
                  checked={consent}
                  onCheckedChange={(v) => setConsent(v === true)}
                />
                <FieldLabel htmlFor="consent" className="font-normal">
                  Jag är vårdnadshavare. Nyckeln stannar i den här telefonen.
                </FieldLabel>
              </Field>

              {hint && !ready ? (
                <FieldDescription>
                  Skriv namnet och kryssa att du är vårdnadshavare.
                </FieldDescription>
              ) : null}

              <Button
                type="button"
                variant="link"
                className="h-auto p-0 text-muted-foreground"
                onClick={() => submit(true)}
              >
                Ingen nyckel? Fortsätt ändå
              </Button>
            </FieldGroup>
          </form>

          <Accordion type="single" collapsible className="w-full">
            <AccordionItem value="pear" className="border-none">
              <AccordionTrigger className="justify-center text-sm text-muted-foreground hover:no-underline">
                Bygger du själv?
              </AccordionTrigger>
              <AccordionContent className="flex flex-col gap-3">
                <p className="text-sm text-muted-foreground">
                  Klistra det här i ChatGPT som instruktion, eller kör Docker.
                </p>
                <pre className="overflow-x-auto rounded-lg bg-foreground p-3 font-mono text-xs text-background whitespace-pre-wrap">
                  {PROMPT}
                </pre>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    navigator.clipboard.writeText(PROMPT)
                    toast("Prompten är kopierad")
                  }}
                >
                  Kopiera prompten
                </Button>
                <pre className="overflow-x-auto rounded-lg bg-foreground p-3 font-mono text-xs text-background whitespace-pre-wrap">
                  {DOCKER}
                </pre>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    navigator.clipboard.writeText(DOCKER)
                    toast("Docker-raden är kopierad")
                  }}
                >
                  Kopiera Docker
                </Button>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </section>
    </Shell>
  )
}
