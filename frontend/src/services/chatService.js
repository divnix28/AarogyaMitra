// frontend/src/services/chatService.js
export const sendChatMessage = async (message) => {
  // Simulating network delay for backend AI response
  await new Promise(resolve => setTimeout(resolve, 600));

  const lowerMsg = message.toLowerCase();

  // Emergency safety trigger (HRRS Escalation rule)
  if (lowerMsg.includes('chest pain') || lowerMsg.includes('breathing') || lowerMsg.includes('severe bleeding')) {
    return {
      text: "⚠️ CRITICAL ALERT: The symptoms you described indicate a potential medical emergency. Please contact emergency services (108) immediately or proceed to the nearest Primary Health Centre.",
      isEmergency: true,
      source: "Official Clinical Guidelines (HRRS Protocol)"
    };
  }

  // General health literacy query handling
  if (lowerMsg.includes('polio') || lowerMsg.includes('vaccine')) {
    return {
      text: "Routine immunization protects children against vaccine-preventable diseases. The upcoming Polio Drop Drive is scheduled for this weekend in District 4.",
      isEmergency: false,
      source: "Verified Health Ministry Knowledge Base"
    };
  }

  return {
    text: "I have recorded your query. For accurate rural triage, please provide specific symptoms like fever duration, cough, or vaccination status.",
    isEmergency: false,
    source: "AarogyaMitra NLU Pipeline"
  };
};