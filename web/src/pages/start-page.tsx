import { useMemo, useState } from "react"
import { ArrowUpIcon, EyeIcon, EyeOffIcon } from "lucide-react"
import { toast } from "sonner"

import Aurora from "@/components/Aurora"
import { BrandMark } from "@/components/brands"
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
  FieldSeparator,
} from "@/components/ui/field"
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from "@/components/ui/input-group"
import { Input } from "@/components/ui/input"
import {
  CLAUDE_OAUTH_BAN,
  DOCKER,
  INTEREST_CHIPS,
  OAUTH,
  PROMPT,
  providerLabel,
  rememberChild,
  saveOAuthSetup,
  saveSetup,
} from "@/lib/setup"

function goPreview() {
  window.location.href = "./test.html"
}

type OauthId = keyof typeof OAUTH

export function StartPage() {
  const [name, setName] = useState("")
  const [key, setKey] = useState("")
  const [consent, setConsent] = useState(false)
  const [showKey, setShowKey] = useState(false)
  const [hint, setHint] = useState(false)
  const [picks, setPicks] = useState<string[]>([])
  const [oauth, setOauth] = useState<OauthId | null>(null)
  const [oauthStatus, setOauthStatus] = useState("")
  const reduceMotion = useMemo(
    () => window.matchMedia("(prefers-reduced-motion: reduce)").matches,
    []
  )

  const child = name.trim().split(/\s+/)[0] || ""
  const ready = consent && child.length >= 2
  const label = providerLabel(key)

  function needReady() {
    if (ready) return true
    setHint(true)
    return false
  }

  function submit(skipKey: boolean) {
    if (!needReady()) return
    saveSetup(child, skipKey ? "" : key.trim(), picks)
    void rememberChild(child, picks)
    goPreview()
  }

  function beginOauth(id: OauthId) {
    if (!needReady()) return
    window.open(OAUTH[id].deviceUrl, "_blank", "noopener,noreferrer")
    setOauth(id)
    setOauthStatus("")
  }

  function enterWithOauth() {
    if (!oauth || !needReady()) return
    saveOAuthSetup(child, oauth, picks)
    void rememberChild(child, picks)
    goPreview()
  }

  async function finishOauth() {
    if (!oauth || !needReady()) return
    try {
      const res = await fetch(`/api/oauth/import/${oauth}`, { method: "POST" })
      if (res.ok) {
        const data = (await res.json()) as { source?: string }
        toast(data.source ? `Hittade inloggningen (${data.source})` : "Inloggningen är sparad här")
        enterWithOauth()
        return
      }
      const data = (await res.json().catch(() => ({}))) as { detail?: string }
      setOauthStatus(
        data.detail ||
          "Ingen lokal session än. Öppna inloggningen, sen tryck igen."
      )
    } catch {
      setOauthStatus(
        "Backend sover. Öppna inloggningen hos dem, eller fortsätt ändå."
      )
    }
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
                <FieldLabel>Vad tänder hen?</FieldLabel>
                <div className="flex flex-wrap gap-2">
                  {INTEREST_CHIPS.map((chip) => {
                    const on = picks.includes(chip)
                    return (
                      <button
                        key={chip}
                        type="button"
                        className={
                          on
                            ? "rounded-full bg-primary px-3 py-1 text-xs text-primary-foreground"
                            : "rounded-full border border-border px-3 py-1 text-xs text-muted-foreground"
                        }
                        onClick={() =>
                          setPicks((cur) =>
                            cur.includes(chip)
                              ? cur.filter((c) => c !== chip)
                              : [...cur, chip]
                          )
                        }
                      >
                        {chip}
                      </button>
                    )
                  })}
                </div>
                <FieldDescription>
                  Inte för att sätta socker på läxan. För att hitta den riktiga
                  dörren in.
                </FieldDescription>
              </Field>

              <Field orientation="horizontal" data-invalid={hint && !consent}>
                <Checkbox
                  id="consent"
                  checked={consent}
                  onCheckedChange={(v) => setConsent(v === true)}
                />
                <FieldLabel htmlFor="consent" className="font-normal">
                  Jag är vårdnadshavare. Inloggningen stannar i den här telefonen.
                </FieldLabel>
              </Field>

              {hint && !ready ? (
                <FieldDescription>
                  Skriv namnet och kryssa att du är vårdnadshavare.
                </FieldDescription>
              ) : null}

              {oauth ? (
                <OauthPanel
                  provider={oauth}
                  status={oauthStatus}
                  onCancel={() => {
                    setOauth(null)
                    setOauthStatus("")
                  }}
                  onDone={() => void finishOauth()}
                  onSkip={enterWithOauth}
                />
              ) : (
                <>
                  <Field>
                    <FieldLabel>Använd abonnemanget</FieldLabel>
                    <div className="flex flex-col gap-2">
                      <Button
                        type="button"
                        variant="outline"
                        className="justify-start gap-2"
                        onClick={() => beginOauth("chatgpt")}
                      >
                        <BrandMark name="chatgpt" />
                        Fortsätt med ChatGPT
                      </Button>
                      <Button
                        type="button"
                        variant="outline"
                        className="justify-start gap-2"
                        onClick={() => beginOauth("grok")}
                      >
                        <BrandMark name="grok" />
                        Fortsätt med Grok
                      </Button>
                      <Button
                        type="button"
                        variant="outline"
                        className="justify-start gap-2"
                        onClick={() => {
                          if (!needReady()) return
                          document.getElementById("key")?.focus()
                          toast("Claude kräver en nyckel. Klistra den här.")
                        }}
                      >
                        <BrandMark name="claude" />
                        Claude — klistra nyckel
                      </Button>
                    </div>
                    <FieldDescription>{CLAUDE_OAUTH_BAN}</FieldDescription>
                  </Field>

                  <FieldSeparator>eller klistra en nyckel</FieldSeparator>

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
                        För den som har en nyckel. Claude hör hemma här.
                      </FieldDescription>
                    )}
                  </Field>

                  <Button
                    type="button"
                    variant="link"
                    className="h-auto p-0 text-muted-foreground"
                    onClick={() => submit(true)}
                  >
                    Ingen nyckel? Fortsätt ändå
                  </Button>
                </>
              )}
            </FieldGroup>
          </form>

          <Accordion type="single" collapsible className="w-full">
            <AccordionItem value="pear" className="border-none">
              <AccordionTrigger className="justify-center text-sm text-muted-foreground hover:no-underline">
                Bygger du själv?
              </AccordionTrigger>
              <AccordionContent className="flex flex-col gap-3">
                <p className="text-sm text-muted-foreground">
                  Päron: `codex login --device-auth` eller `grok login --device-auth`,
                  sen “Jag är inne”. Eller klistra prompten i ChatGPT.
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

function OauthPanel({
  provider,
  status,
  onCancel,
  onDone,
  onSkip,
}: {
  provider: OauthId
  status: string
  onCancel: () => void
  onDone: () => void
  onSkip: () => void
}) {
  const spec = OAUTH[provider]
  return (
    <Field>
      <FieldLabel>Logga in hos {spec.label}</FieldLabel>
      <p className="text-sm text-muted-foreground">
        En länk, som Hermes. Logga in hos dem, sen Jag är inne.
      </p>
      <p className="text-sm text-muted-foreground">{spec.hint}</p>
      <div className="flex flex-col gap-2">
        <Button
          type="button"
          variant="outline"
          onClick={() =>
            window.open(spec.deviceUrl, "_blank", "noopener,noreferrer")
          }
        >
          Öppna {spec.label}
        </Button>
        <Button type="button" onClick={onDone}>
          Jag är inne
        </Button>
        {status ? (
          <Button
            type="button"
            variant="link"
            className="h-auto p-0 text-muted-foreground"
            onClick={onSkip}
          >
            Fortsätt ändå
          </Button>
        ) : null}
        <Button type="button" variant="ghost" onClick={onCancel}>
          Avbryt
        </Button>
      </div>
      {status ? <FieldDescription>{status}</FieldDescription> : null}
    </Field>
  )
}
