export type TelegramStatus = {
  username?: string | null
  invite?: string | null
  linked?: boolean
  ready?: boolean
}

export async function telegramStatus(): Promise<TelegramStatus> {
  try {
    const res = await fetch("/api/telegram")
    if (res.ok) return (await res.json()) as TelegramStatus
  } catch {
    /* backend sover */
  }
  return {}
}

export async function bindTelegram(token: string): Promise<TelegramStatus & { detail?: string }> {
  try {
    const res = await fetch("/api/telegram/bind", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token }),
    })
    const data = (await res.json().catch(() => ({}))) as TelegramStatus & {
      detail?: string
    }
    if (!res.ok) {
      return { detail: data.detail || "Tokenen gick inte att använda." }
    }
    return data
  } catch {
    return {
      detail: "Backend sover. Klistra token när Utter körs hemma, inte till en främmande bot.",
    }
  }
}
