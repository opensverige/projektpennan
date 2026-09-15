import { ChatPage } from "@/pages/chat-page"
import { GuardianPage } from "@/pages/guardian-page"
import { StartPage } from "@/pages/start-page"

function currentPage() {
  const file = window.location.pathname.split("/").pop() || ""
  if (file.startsWith("start")) return "start"
  if (file.startsWith("guardian")) return "guardian"
  return "chat"
}

export function App() {
  const page = currentPage()
  if (page === "start") return <StartPage />
  if (page === "guardian") return <GuardianPage />
  return <ChatPage />
}

export default App
