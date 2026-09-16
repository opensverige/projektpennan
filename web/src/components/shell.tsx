import type { ReactNode } from "react"
import { SparklesIcon } from "lucide-react"

import { Button } from "@/components/ui/button"

export function Shell({
  children,
  current,
}: {
  children: ReactNode
  current: "start" | "chat" | "guardian" | "test"
}) {
  return (
    <div className="flex min-h-svh flex-col">
      <header className="relative z-10 flex items-center justify-between gap-3 px-4 py-3">
        <a href="./index.html" className="flex items-center gap-2 font-medium">
          <span className="flex size-7 items-center justify-center rounded-md bg-primary text-primary-foreground">
            <SparklesIcon />
          </span>
          Gnista
        </a>
        <nav className="flex items-center gap-1">
          <Button asChild variant={current === "start" ? "secondary" : "ghost"} size="sm">
            <a href="./start.html">Sätt upp</a>
          </Button>
          <Button asChild variant={current === "test" ? "secondary" : "ghost"} size="sm">
            <a href="./test.html">Testa</a>
          </Button>
          <Button asChild variant={current === "chat" ? "secondary" : "ghost"} size="sm">
            <a href="./index.html">Chatten</a>
          </Button>
          <Button asChild variant={current === "guardian" ? "secondary" : "ghost"} size="sm">
            <a href="./guardian.html">Föräldravy</a>
          </Button>
        </nav>
      </header>
      {children}
    </div>
  )
}
