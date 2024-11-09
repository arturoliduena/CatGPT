export const fetchMunicipalities = async () => {
  const res = await fetch("http://localhost:8000/municipalities");
  return res.json();
};

export const sendAlert = async (
  municipeCode: string,
  alertMessage: string,
  severity: string,
  targetAudience: string
) => {
  const res = await fetch("http://localhost:8000/generate-alert", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      municipe_code: municipeCode,
      alert_message: alertMessage,
      severity: severity,
      target_audience: targetAudience,
    }),
  });
  return res.json();
};
