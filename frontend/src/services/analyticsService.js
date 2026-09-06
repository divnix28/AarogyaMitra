export const fetchDashboardData = async () => {
  // Simulating a network delay to test loading screens
  await new Promise(resolve => setTimeout(resolve, 800));

  return {
    healthLiteracy: {
      averageScore: 78,
      totalInteractions: 12450,
      topTopics: ["Vaccination", "Maternal Care", "Nutrition"]
    },
    symptomTrends: [
      { symptom: "Fever & Chills", count: 840, trend: "up" },
      { symptom: "Chest Pain", count: 120, trend: "stable" },
    ],
    officialAlerts: [
      { id: 1, title: "Polio Drop Drive - District 4", severity: "high", verified: true }
    ],
    communitySignals: [
      { id: 2, title: "Unusual increase in 'Dengue' queries in Sector 9", severity: "medium", verified: false }
    ],
    aiSystemHealth: {
      gatePassed: true,
      accuracy: 82.4
    }
  };
};