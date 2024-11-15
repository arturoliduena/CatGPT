"use client";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Send, Shield, Play, Pause, Square } from "lucide-react";
import dynamic from "next/dynamic";
import { useMemo, useState } from "react";
import { Municipalities, Municipality } from "./municipalities";
import { MultiSelect } from "./ui/multi-select";
import {
  fetchFloodZones,
  fetchPOI,
  FloodableZone,
  POI,
  sendAlert,
} from "@/lib/queries";
import { ClipLoader } from "react-spinners";
import Markdown from "react-markdown";

const languageOptions = [
  { label: "Espanyol", value: "Spanish" },
  { label: "Anglès", value: "English" },
  { label: "Euskera", value: "Euskera" },
  { label: "Gallec", value: "Galician" },
  { label: "Aranès", value: "Aranese" },
  { label: "Aragonès", value: "Aragonese" },
  { label: "Asturià", value: "Asturian" },
];

const languageMap = {
  Catalan: "Català",
  Spanish: "Espanyol",
  English: "Anglès",
  Euskera: "Euskera",
  Galician: "Gallec",
  Aranese: "Aranès",
  Aragonese: "Aragonès",
  Asturian: "Asturià",
};

export function FloodGuard() {
  const [situation, setSituation] = useState("");
  const [severity, setSeverity] = useState("moderada");
  const [audience, setAudience] = useState("general");
  const [showLanguage, setShowLanguage] = useState("Catalan");
  const [languages, setLanguages] = useState<string[]>([]);
  const [generatedAlert, setGeneratedAlert] = useState<{
    [key: string]: string;
  }>();
  const [bounds, setBounds] = useState<[[number, number], [number, number]]>([
    [41.324, 2.083],
    [41.424, 2.223],
  ]);

  const [floodableZones, setFloodableZones] = useState<FloodableZone[]>([]);
  const [poi, setPoi] = useState<POI[]>([]);

  const [selectedMunicipality, setSelectedMunicipality] =
    useState<Municipality>();
  const [isGenerating, setIsGenerating] = useState(false);

  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [audio, setAudio] = useState<HTMLAudioElement | null>(null);

  const handlePlay = () => {
    if (audio) {
      audio.play();
    }
  };

  const handlePause = () => {
    if (audio) {
      audio.pause();
    }
  };

  const handleStop = () => {
    if (audio) {
      audio.pause();
      audio.currentTime = 0;
    }
  };

  const handleGenerateAlert = async () => {
    setIsGenerating(true);
    setGeneratedAlert(undefined);
    let hasError = false;

    if (!selectedMunicipality) {
      alert("Seleccioneu una ciutat.");
      hasError = true;
    }
    if (!situation) {
      alert("Descriviu la situació d'inundació.");
      hasError = true;
    }
    if (!severity) {
      alert("Seleccioneu la severitat de l'alerta.");
      hasError = true;
    }
    if (!audience) {
      alert("Seleccioneu el públic objectiu.");
      hasError = true;
    }

    if (hasError || !selectedMunicipality) {
      setIsGenerating(false);
      return;
    }

    try {
      const response = await sendAlert(
        selectedMunicipality.codiMunicipi,
        selectedMunicipality.nomMunicipi,
        situation,
        severity,
        audience,
        languages.join(",")
      );
      console.log("Alert generated:", response);
      console.log("------>", response);
      setGeneratedAlert(response.alerts);
      if (response.audioUrl) {
        setAudioUrl(response.audioUrl);
        setAudio(new Audio(response.audioUrl));
      }
    } catch (error) {
      console.error("Error generating alert:", error);
      alert("Hi ha hagut un error en generar l'alerta.");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSelectMunicipality = async (municipality: Municipality) => {
    setBounds([
      [municipality.bbox.ymin, municipality.bbox.xmin],
      [municipality.bbox.ymax, municipality.bbox.xmax],
    ]);
    setSelectedMunicipality(municipality);
    const floodZonesResult = await fetchFloodZones(municipality.codiMunicipi);
    setFloodableZones(floodZonesResult);

    const poiResult = await fetchPOI(municipality.codiMunicipi);
    setPoi(poiResult);
  };

  const Map = useMemo(
    () =>
      dynamic(() => import("@/components/map"), {
        loading: () => <p>A map is loading</p>,
        ssr: false,
      }),
    []
  );

  return (
    <div className="flex h-screen bg-gray-100">
      <div className="w-1/2 p-4 overflow-y-auto">
        <Card className="shadow-lg h-full overflow-y-auto">
          <CardHeader className="bg-primary text-primary-foreground">
            <CardTitle className="text-2xl flex items-center">
              <Shield className="mr-2" /> FloodGuard: Sistema d'Alerta
              Comunitària
            </CardTitle>
            <CardDescription className="text-primary-foreground/80">
              Protegiu la vostra comunitat amb alertes d'inundació a temps
            </CardDescription>
          </CardHeader>
          <CardContent className="mt-4 space-y-6 overflow-y-auto">
            <div>
              <Label htmlFor="city" className="text-lg font-semibold">
                Ciutat
              </Label>
              <div className="flex mt-1 space-x-2">
                <Municipalities
                  onSelectMunicipality={handleSelectMunicipality}
                />
              </div>
            </div>
            <div>
              <Label htmlFor="situation" className="text-lg font-semibold">
                Situació d'Alerta
              </Label>
              <Textarea
                id="situation"
                placeholder="Descriviu la situació d'inundació..."
                value={situation}
                onChange={(e) => setSituation(e.target.value)}
                className="mt-1"
                rows={4}
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="severity" className="text-lg font-semibold">
                  Severitat de l'Alerta
                </Label>
                <Select value={severity} onValueChange={setSeverity}>
                  <SelectTrigger id="severity" className="mt-1">
                    <SelectValue placeholder="Seleccioneu la severitat" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="baixa">Baixa</SelectItem>
                    <SelectItem value="moderada">Moderada</SelectItem>
                    <SelectItem value="alta">Alta</SelectItem>
                    <SelectItem value="extrema">Extrema</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="audience" className="text-lg font-semibold">
                  Públic Objectiu
                </Label>
                <Select value={audience} onValueChange={setAudience}>
                  <SelectTrigger id="audience" className="mt-1">
                    <SelectValue placeholder="Seleccioneu el públic" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="general">Públic General</SelectItem>
                    <SelectItem value="serveis d'emergencia">
                      Serveis d'Emergència
                    </SelectItem>
                    <SelectItem value="autoritats locals">
                      Autoritats Locals
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div>
              <Label htmlFor="languages" className="text-lg font-semibold">
                Opcions de Traducció
              </Label>
              <MultiSelect
                options={languageOptions}
                onValueChange={setLanguages}
                defaultValue={languages}
                placeholder="Seleccioneu els idiomes"
                variant="inverted"
                animation={2}
                maxCount={3}
              />
            </div>
            <Button
              onClick={handleGenerateAlert}
              className="w-full"
              disabled={isGenerating}
            >
              {isGenerating ? (
                <ClipLoader size={20} color={"#ffffff"} />
              ) : (
                <Send className="mr-2 h-4 w-4" />
              )}
              Generar Alerta
            </Button>
            {generatedAlert && (
              <div className="mt-4 p-4 rounded-lg border border-gray-200">
                {Object.keys(generatedAlert).length >= 1 && (
                  <div className="flex items-center justify-between p-1 space-x-2">
                    <Select
                      value={showLanguage}
                      onValueChange={setShowLanguage}
                    >
                      <SelectTrigger id="showlanguage" className="mt-1">
                        <SelectValue placeholder="Idioma a visualitzar" />
                      </SelectTrigger>
                      <SelectContent>
                        {Object.keys(generatedAlert).map((d) => (
                          <SelectItem key={d} value={d}>
                            {languageMap[d] || d}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    {showLanguage === "Catalan" && audioUrl && (
                      <div className="flex space-x-1 items-center justify-center">
                        <Button onClick={handlePlay} className="h-7 w-6">
                          <Play className="h-3 w-3" />
                        </Button>
                        <Button onClick={handlePause} className="h-7 w-6">
                          <Pause className="h-3 w-3" />
                        </Button>
                        <Button onClick={handleStop} className="h-7 w-6">
                          <Square className="h-3 w-3" />
                        </Button>
                      </div>
                    )}
                  </div>
                )}

                <div className="text-gray-900 p-1">
                  {generatedAlert[showLanguage]
                    .split("\n")
                    .map((line, index) => (
                      <p key={index}>{line || <br />}</p>
                    ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
      <div className="w-1/2 h-screen">
        <Map initialBounds={bounds} floodableZones={floodableZones} poi={poi} />
      </div>
    </div>
  );
}
