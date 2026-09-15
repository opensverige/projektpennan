import { useRef } from "react"
import "drawably/style.css"
import "@/land.css"
import {
  DrawablyArrow,
  DrawablyBadge,
  DrawablyDivider,
  DrawablyHighlight,
  DrawablyList,
  DrawablyTooltip,
} from "drawably/react"

export function LandPage() {
  const parentRef = useRef<HTMLSpanElement>(null)
  const startRef = useRef<HTMLAnchorElement>(null)

  return (
    <div className="land">
      <main>
        <section className="land-block">
          <div className="land-badges">
            <DrawablyBadge>åk 4–6</DrawablyBadge>
            <DrawablyBadge>hemma</DrawablyBadge>
            <DrawablyBadge>öppen</DrawablyBadge>
          </div>
          <h1>Gnista</h1>
          <p className="land-lead">
            En studiekompis. Frågor, inte facit.{" "}
            <DrawablyHighlight fill="#f0c94d">
              <span ref={parentRef}>Föräldern</span>
            </DrawablyHighlight>{" "}
            äger plattan.
          </p>
        </section>

        <DrawablyDivider />

        <section className="land-block">
          <p className="land-kicker">Så funkar det</p>
          <DrawablyList marker="dash" className="land-list">
            <li>Barnet får en fråga. Aldrig svaret först.</li>
            <li>Reglerna sitter i koden. Inte i prompten.</li>
            <li>Ni kör den hemma. Vi ser inte chatten.</li>
          </DrawablyList>
        </section>

        <DrawablyDivider />

        <section className="land-block">
          <p className="land-kicker">Öppna</p>
          <p className="land-lead">
            En skärm. Namn. Sen chatten. Ingen QR. Inget barnkonto.
          </p>
          <div className="land-go-row">
            <a ref={startRef} className="land-go" href="./start.html">
              Sätt igång
            </a>
            <DrawablyTooltip to={startRef} className="land-tip">
              Ingen nyckel behövs
            </DrawablyTooltip>
          </div>
          <DrawablyArrow from={parentRef} to={startRef} />
          <a
            className="land-git"
            href="https://github.com/opensverige/projektpennan"
          >
            GitHub
          </a>
        </section>
      </main>
    </div>
  )
}
