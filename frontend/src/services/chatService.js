// frontend/src/services/chatService.js

const getSessionId = () => {
  let sessionId = sessionStorage.getItem("aarogyamitra_session");
  if (!sessionId) {
    sessionId = "user_" + Math.random().toString(36).substring(2, 10);
    sessionStorage.setItem("aarogyamitra_session", sessionId);
  }
  return sessionId;
};

const API_URL = "http://localhost:8000/api/v1/chat/message";

export const sendChatMessage = async (message) => {
  const senderId = getSessionId();

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        channel: "web",
        user_id: senderId,
        message,
        language: "en",
        timestamp: new Date().toISOString(),
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP ${response.status}: ${errorText || "Backend request failed"}`);
    }

    const data = await response.json();

    console.log("Full Backend Response:", data);

    const action = String(data.action || "").toUpperCase();
    const isEmergency = Boolean(data.isEmergency) || data.intent === "emergency" || ["ESCALATE", "ESCALATE_TO_HUMAN"].includes(action);

    return {
      text: data.message || data.response || data.answer || data.reply || data.text || "Text missing from backend response.",
      isEmergency,
      source: data.source || "AarogyaMitra Core Backend"
    };

  } catch (error) {
    console.error("Backend API Error:", error);
    return {
      text: "⚠️ Connection error. Please make sure the Python backend is running on port 8000.",
      isEmergency: true,
      source: "System Error"
    };
  }
};