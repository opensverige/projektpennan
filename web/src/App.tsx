import { ChatPage } from "@/pages/chat-page"
import { GuardianPage } from "@/pages/guardian-page"
import { LandPage } from "@/pages/land-page"
import { StartPage } from "@/pages/start-page"
import { TestPage } from "@/pages/test-page"

function currentPage() {
  const file = window.location.pathname.split("/").pop() || ""
  if (file.startsWith("land")) return "land"
  if (file.startsWith("start")) return "start"
  if (file.startsWith("guardian")) return "guardian"
  if (file.startsWith("test")) return "test"
  return "chat"
}

export function App() {
  const page = currentPage()
  if (page === "land") return <LandPage />
  if (page === "start") return <StartPage />
  if (page === "guardian") return <GuardianPage />
  if (page === "test") return <TestPage />
  return <ChatPage />
}

export default App
