import { StringifyOptions } from "querystring";

export const fetchMunicipalities = async () => {
  const res = await fetch("http://localhost:8000/municipalities");
  return res.json();
};

export interface FloodableZone {
  municipalityName: string;
  municipalityCode: string;
  geom: string;
}
export const fetchFloodZones = async (codeMunicipality: string) => {
  const res = await fetch(
    `http://localhost:8000/municipalities/${codeMunicipality}/floodzones`
  );
  return res.json() as Promise<FloodableZone[]>;
};

export interface POI {
  municipalityName: string;
  municipalityCode: string;
  amenity: string;
  floodable: boolean;
  name: string;
  lon: string;
  lat: string;
}

export const fetchPOI = async (codeMunicipality: string) => {
  const res = await fetch(
    `http://localhost:8000/municipalities/${codeMunicipality}/poi`
  );
  return res.json() as Promise<POI[]>;
};

export const sendAlert = async (
  municipeCode: string,
  municipeName: string,
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
      municipe_name: municipeName,
      alert_message: alertMessage,
      severity: severity,
      target_audience: targetAudience,
    }),
  });
  return res.json();
};
