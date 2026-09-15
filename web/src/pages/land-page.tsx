import { useRef } from "react"
import "drawably/style.css"
import "@/land.css"
import {
  DrawablyArrow,
  DrawablyDivider,
  DrawablyHighlight,
  DrawablyList,
} from "drawably/react"

const ink = "#171717"

export function LandPage() {
  const parentRef = useRef<HTMLSpanElement>(null)
  const startRef = useRef<HTMLAnchorElement>(null)

  return (
    <div className="land">
      <main>
        <section className="land-block">
          <h1>Gnista</h1>
          <p className="land-lead">
            En studiekompis. Frågor, inte facit.{" "}
            <DrawablyHighlight fill="#f0c94d">
              <span ref={parentRef}>Föräldern</span>
            </DrawablyHighlight>{" "}
            äger plattan.
          </p>
          <a ref={startRef} className="land-go" href="./start.html">
            Sätt igång
          </a>
          <DrawablyArrow from={parentRef} to={startRef} stroke={ink} fill={ink} />
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
