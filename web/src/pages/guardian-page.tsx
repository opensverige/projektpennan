import { useEffect, useState } from "react"

import { Shell } from "@/components/shell"
import { Badge } from "@/components/ui/badge"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"

type Report = {
  id: string
  title: string
  period?: string
  summary?: string
  highlights?: string[]
  todo?: string[]
  notes?: string
}

export function GuardianPage() {
  const [reports, setReports] = useState<Report[] | null>(null)
  const [active, setActive] = useState<Report | null>(null)
  const [error, setError] = useState(false)

  useEffect(() => {
    fetch("/api/reports")
      .then((r) => r.json())
      .then((data: { reports?: Report[] }) => {
        setReports(data.reports || [])
      })
      .catch(() => {
        setError(true)
        setReports([])
      })
  }, [])

  async function openReport(id: string) {
    const res = await fetch(`/api/reports/${id}`)
    if (!res.ok) return
    setActive((await res.json()) as Report)
  }

  return (
    <Shell current="guardian">
      <div className="mx-auto grid w-full max-w-5xl flex-1 gap-4 px-4 py-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Rapporter</CardTitle>
            <CardDescription>Det du ser här stannar hemma.</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-2">
            {reports === null ? (
              <p className="text-sm text-muted-foreground">Laddar…</p>
            ) : error ? (
              <p className="text-sm text-muted-foreground">
                Kunde inte läsa rapporter. Starta backend om du vill se dem.
              </p>
            ) : reports.length === 0 ? (
              <p className="text-sm text-muted-foreground">
                Inga rapporter ännu. Det är okej.
              </p>
            ) : (
              reports.map((report) => (
                <button
                  key={report.id}
                  type="button"
                  onClick={() => void openReport(report.id)}
                  className="rounded-lg border border-border px-3 py-3 text-left hover:bg-muted"
                >
                  <p className="font-medium">{report.title}</p>
                  {report.period ? (
                    <p className="text-xs text-muted-foreground">{report.period}</p>
                  ) : null}
                </button>
              ))
            )}
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>{active ? active.title : "Välj en rapport"}</CardTitle>
            {active?.period ? (
              <CardDescription>
                <Badge variant="secondary">{active.period}</Badge>
              </CardDescription>
            ) : (
              <CardDescription>När du klickar en i listan visas den här.</CardDescription>
            )}
          </CardHeader>
          <CardContent className="flex flex-col gap-3 text-sm">
            {active ? (
              <>
                <p>{active.summary}</p>
                {active.highlights?.length ? (
                  <>
                    <Separator />
                    <p className="font-medium">Höjdpunkter</p>
                    <ul className="list-disc pl-5">
                      {active.highlights.map((item) => (
                        <li key={item}>{item}</li>
                      ))}
                    </ul>
                  </>
                ) : null}
                {active.todo?.length ? (
                  <>
                    <p className="font-medium">Att göra</p>
                    <ul className="list-disc pl-5">
                      {active.todo.map((item) => (
                        <li key={item}>{item}</li>
                      ))}
                    </ul>
                  </>
                ) : null}
                {active.notes ? <p>{active.notes}</p> : null}
              </>
            ) : null}
          </CardContent>
        </Card>
      </div>
    </Shell>
  )
}
