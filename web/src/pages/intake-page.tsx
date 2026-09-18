import { useMemo, useState } from "react"

import Aurora from "@/components/Aurora"
import { Shell } from "@/components/shell"
import { Button } from "@/components/ui/button"
import { Field, FieldDescription, FieldLabel } from "@/components/ui/field"
import { Textarea } from "@/components/ui/textarea"
import {
  ENERGY_CHIPS,
  GRADE_CHIPS,
  HELP_CHIPS,
  INTEREST_CHIPS,
  LANGUAGE_CHIPS,
  STRUGGLE_CHIPS,
  loadSetup,
  patchSetup,
  rememberIntake,
} from "@/lib/setup"
import { cn } from "@/lib/utils"

type Step = {
  id: string
  question: string
  hint?: string
  chips: readonly string[]
  max: number
}

const STEPS: Step[] = [
  {
    id: "grade",
    question: "Vilken årskurs?",
    chips: GRADE_CHIPS,
    max: 1,
  },
  {
    id: "language",
    question: "Hur ska sidekicken prata?",
    hint: "Hur hen använder språket. Inte var ni kommer ifrån.",
    chips: LANGUAGE_CHIPS,
    max: 1,
  },
  {
    id: "interests",
    question: "Vad tänder hen just nu?",
    hint: "Högst två. Dörren in, inte belöning ovanpå läxan.",
    chips: INTEREST_CHIPS,
    max: 2,
  },
  {
    id: "struggle",
    question: "Vad kärvar oftast?",
    chips: STRUGGLE_CHIPS,
    max: 1,
  },
  {
    id: "energy",
    question: "Hur är orken efter skolan?",
    chips: ENERGY_CHIPS,
    max: 1,
  },
  {
    id: "helps",
    question: "Vad hjälper när det kärvar?",
    hint: "Högst två. Behov, inte en diagnos.",
    chips: HELP_CHIPS,
    max: 2,
  },
]

function goPreview() {
  window.location.href = "./test.html"
}

function Chip({
  label,
  on,
  onClick,
}: {
  label: string
  on: boolean
  onClick: () => void
}) {
  return (
    <button
      type="button"
      className={cn(
        "rounded-full px-4 py-2 text-sm",
        on
          ? "bg-primary text-primary-foreground"
          : "border border-border text-foreground"
      )}
      onClick={onClick}
    >
      {label}
    </button>
  )
}

export function IntakePage() {
  const setup = loadSetup()
  const [step, setStep] = useState(0)
  const [grade, setGrade] = useState("")
  const [language, setLanguage] = useState("")
  const [interests, setInterests] = useState<string[]>([])
  const [struggle, setStruggle] = useState("")
  const [energy, setEnergy] = useState("")
  const [helps, setHelps] = useState<string[]>([])
  const [note, setNote] = useState("")
  const [noteOpen, setNoteOpen] = useState(false)
  const reduceMotion = useMemo(
    () => window.matchMedia("(prefers-reduced-motion: reduce)").matches,
    []
  )

  if (!setup?.child || !setup.consent) {
    window.location.replace("./start.html")
    return null
  }

  const onNote = step >= STEPS.length
  const current = STEPS[step]
  const picked: Record<string, string | string[]> = {
    grade,
    language,
    interests,
    struggle,
    energy,
    helps,
  }

  function toggle(id: string, chip: string, max: number) {
    if (max === 1) {
      if (id === "grade") setGrade(chip)
      if (id === "language") setLanguage(chip)
      if (id === "struggle") setStruggle(chip)
      if (id === "energy") setEnergy(chip)
      return
    }
    const setter = id === "interests" ? setInterests : setHelps
    setter((cur) => {
      if (cur.includes(chip)) return cur.filter((c) => c !== chip)
      if (cur.length >= max) return [...cur.slice(1), chip]
      return [...cur, chip]
    })
  }

  function canAdvance() {
    if (onNote) return true
    const value = picked[current.id]
    if (Array.isArray(value)) return value.length > 0
    return Boolean(value)
  }

  async function finish(skipNote: boolean) {
    const payload = {
      name: setup!.child,
      interests,
      grade,
      language,
      struggle,
      energy,
      helps,
      note: skipNote ? "" : note.trim(),
    }
    patchSetup({
      interests,
      grade,
      language,
      struggle,
      energy,
      helps,
      note: payload.note,
    })
    await rememberIntake(payload)
    goPreview()
  }

  return (
    <Shell current="start">
      <section className="relative flex flex-1 flex-col items-center justify-center px-4 pb-10">
        {!reduceMotion ? (
          <div className="pointer-events-none absolute inset-0 -z-10 overflow-hidden">
            <Aurora
              lightMode
              amplitude={0.7}
              blend={0.5}
              speed={0.3}
              colorStops={["#c4b5a0", "#9aa4b2", "#a8c3b5"]}
            />
          </div>
        ) : (
          <div className="absolute inset-0 -z-10 bg-muted" />
        )}

        <div className="flex w-full max-w-sm flex-col gap-6">
          <p className="text-sm text-muted-foreground">
            För {setup.child}. Inte för hen att fylla i.
          </p>

          {onNote ? (
            <div className="flex flex-col gap-4 rounded-xl border border-border bg-background/90 px-6 py-7 shadow-md backdrop-blur-sm">
              <Field>
                <FieldLabel>Något vi ska veta?</FieldLabel>
                <FieldDescription>
                  Skriv hur hen lär sig bäst. Inte en diagnos.
                </FieldDescription>
                {noteOpen ? (
                  <Textarea
                    value={note}
                    maxLength={400}
                    rows={3}
                    placeholder="Kortare pass. Läs högt."
                    onChange={(e) => setNote(e.target.value)}
                  />
                ) : null}
              </Field>
              <Button type="button" onClick={() => void finish(true)}>
                Hoppa över
              </Button>
              {noteOpen ? (
                <Button
                  type="button"
                  variant="outline"
                  disabled={!note.trim()}
                  onClick={() => void finish(false)}
                >
                  Spara anteckningen
                </Button>
              ) : (
                <Button
                  type="button"
                  variant="ghost"
                  onClick={() => setNoteOpen(true)}
                >
                  Kort anteckning
                </Button>
              )}
              <Button
                type="button"
                variant="link"
                className="h-auto p-0 text-muted-foreground"
                onClick={() => setStep(STEPS.length - 1)}
              >
                Tillbaka
              </Button>
            </div>
          ) : (
            <div className="flex flex-col gap-5 rounded-xl border border-border bg-background/90 px-6 py-7 shadow-md backdrop-blur-sm">
              <Field>
                <FieldLabel>{current.question}</FieldLabel>
                {current.hint ? (
                  <FieldDescription>{current.hint}</FieldDescription>
                ) : null}
                <div className="flex flex-wrap gap-2">
                  {current.chips.map((chip) => {
                    const value = picked[current.id]
                    const on = Array.isArray(value)
                      ? value.includes(chip)
                      : value === chip
                    return (
                      <Chip
                        key={chip}
                        label={chip}
                        on={on}
                        onClick={() => toggle(current.id, chip, current.max)}
                      />
                    )
                  })}
                </div>
              </Field>
              <div className="flex items-center justify-between">
                {step > 0 ? (
                  <Button
                    type="button"
                    variant="ghost"
                    onClick={() => setStep((s) => s - 1)}
                  >
                    Tillbaka
                  </Button>
                ) : (
                  <span />
                )}
                <Button
                  type="button"
                  disabled={!canAdvance()}
                  onClick={() => setStep((s) => s + 1)}
                >
                  Fortsätt
                </Button>
              </div>
            </div>
          )}
        </div>
      </section>
    </Shell>
  )
}
