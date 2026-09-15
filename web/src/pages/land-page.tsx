import "drawably/style.css"
import "drawably/font.css"
import "@/land.css"
import {
  DrawablyBadge,
  DrawablyButton,
  DrawablyCard,
  DrawablyCircle,
  DrawablyDivider,
  DrawablyHighlight,
  DrawablyList,
  DrawablyUnderline,
} from "drawably/react"

function goStart() {
  window.location.href = "./start.html"
}

export function LandPage() {
  return (
    <div className="land">
      <main>
        <section className="land-block">
          <DrawablyBadge variant="scribble">skiss</DrawablyBadge>
          <h1>
            <DrawablyCircle>Gnista</DrawablyCircle>
          </h1>
          <p className="land-lead">
            En studiekompis för åk 4–6.{" "}
            <DrawablyUnderline>Frågor</DrawablyUnderline>, inte facit.{" "}
            <DrawablyHighlight>Föräldern</DrawablyHighlight> äger plattan.
          </p>
          <DrawablyButton variant="solid" onClick={goStart}>
            Sätt igång
          </DrawablyButton>
        </section>

        <DrawablyDivider />

        <section className="land-block">
          <p className="land-kicker">Så funkar det</p>
          <DrawablyCard className="land-card">
            <DrawablyList marker="dash">
              <li>Barnet får en fråga. Aldrig svaret först.</li>
              <li>Reglerna sitter i koden. Inte i prompten.</li>
              <li>Ni kör den hemma. Vi ser inte chatten.</li>
            </DrawablyList>
          </DrawablyCard>
        </section>

        <DrawablyDivider />

        <section className="land-block">
          <p className="land-kicker">Öppna</p>
          <p className="land-lead">
            En skärm. Namn. Sen chatten. Ingen QR. Inget barnkonto.
          </p>
          <DrawablyButton variant="scribble" onClick={goStart}>
            Jag är föräldern
          </DrawablyButton>
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
