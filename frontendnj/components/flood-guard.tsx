"use client";

import { useState, useEffect, useMemo } from "react";
import { MapContainer, TileLayer, Marker, useMap } from "react-leaflet";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from "@/components/ui/command";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import {
  AlertTriangle,
  Check,
  ChevronsUpDown,
  MapPin,
  Languages,
  Send,
  Shield,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Municipalities } from "./municipalities";
import dynamic from "next/dynamic";

// Placeholder function for fetching dynamic metrics
const fetchDynamicMetrics = async (city: string) => {
  // This would typically be an API call
  return {
    weatherCondition: "Pluja Forta",
    waterLevel: "2.5m",
    rainFall: "100mm/hr",
  };
};

// Placeholder function for generating alert with LLM
const generateAlertWithLLM = async (
  situation: string,
  metrics: any,
  customizations: any
) => {
  // This would typically involve an API call to an LLM service
  return `ALERTA D'INUNDACIÓ: ${situation} a ${customizations.city}. Nivell d'aigua actual: ${metrics.waterLevel}. Severitat: ${customizations.severity}. Mantingueu-vos segur i seguiu les instruccions de les autoritats locals.`;
};

const languageOptions = [
  { label: "Catalan", value: "Catalan" },
  { label: "Spanish", value: "Spanish" },
  { label: "English", value: "English" },
];

export function FloodGuard() {
  const [city, setCity] = useState("Barcelona");
  const [situation, setSituation] = useState("");
  const [severity, setSeverity] = useState("moderate");
  const [audience, setAudience] = useState("general");
  const [languages, setLanguages] = useState<string[]>([]);
  const [generatedAlert, setGeneratedAlert] = useState("");
  const [openLanguages, setOpenLanguages] = useState(false);

  const handleGenerateAlert = async () => {
    const metrics = await fetchDynamicMetrics(city);
    const customizations = { city, severity, audience };
    const alert = await generateAlertWithLLM(
      situation,
      metrics,
      customizations
    );
    setGeneratedAlert(alert);
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
        <Card className="shadow-lg h-full">
          <CardHeader className="bg-primary text-primary-foreground">
            <CardTitle className="text-2xl flex items-center">
              <Shield className="mr-2" /> FloodGuard: Sistema d'Alerta
              Comunitària
            </CardTitle>
            <CardDescription className="text-primary-foreground/80">
              Protegiu la vostra comunitat amb alertes d'inundació a temps
            </CardDescription>
          </CardHeader>
          <CardContent className="mt-4 space-y-6">
            <div>
              <Label htmlFor="city" className="text-lg font-semibold">
                Ciutat
              </Label>
              <div className="flex mt-1 space-x-2">
                <Municipalities />
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
                    <SelectItem value="low">Baixa</SelectItem>
                    <SelectItem value="moderate">Moderada</SelectItem>
                    <SelectItem value="high">Alta</SelectItem>
                    <SelectItem value="extreme">Extrema</SelectItem>
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
                    <SelectItem value="emergency">
                      Serveis d'Emergència
                    </SelectItem>
                    <SelectItem value="authorities">
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
              <Popover open={openLanguages} onOpenChange={setOpenLanguages}>
                <PopoverTrigger asChild>
                  <Button
                    variant="outline"
                    role="combobox"
                    aria-expanded={openLanguages}
                    className="w-full justify-between mt-1"
                  >
                    <Languages className="mr-2 h-4 w-4" />
                    {Array.isArray(languages) && languages.length > 0
                      ? `${languages.length} seleccionats`
                      : "Seleccioneu idiomes..."}
                    <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="w-full p-0">
                  <Command>
                    <CommandInput placeholder="Cerca idiomes..." />
                    <CommandEmpty>No s'ha trobat cap idioma.</CommandEmpty>
                    <CommandGroup>
                      {languageOptions.map((language) => (
                        <CommandItem
                          key={language.value}
                          onSelect={() => {
                            setLanguages((prev) => {
                              const newLanguages = Array.isArray(prev)
                                ? prev
                                : [];
                              return newLanguages.includes(language.value)
                                ? newLanguages.filter(
                                    (l) => l !== language.value
                                  )
                                : [...newLanguages, language.value];
                            });
                            setOpenLanguages(true);
                          }}
                        >
                          <Check
                            className={cn(
                              "mr-2 h-4 w-4",
                              Array.isArray(languages) &&
                                languages.includes(language.value)
                                ? "opacity-100"
                                : "opacity-0"
                            )}
                          />
                          {language.label}
                        </CommandItem>
                      ))}
                    </CommandGroup>
                  </Command>
                </PopoverContent>
              </Popover>
            </div>
            <Button onClick={handleGenerateAlert} className="w-full">
              <Send className="mr-2 h-4 w-4" /> Generar Alerta
            </Button>
            {generatedAlert && (
              <div className="mt-4 p-4 bg-yellow-100 rounded-lg border border-yellow-300">
                <h3 className="font-bold text-lg mb-2 text-yellow-800">
                  Alerta Generada:
                </h3>
                <p className="text-yellow-900">{generatedAlert}</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
      <div className="w-1/2 h-screen">
        <Map />
      </div>
    </div>
  );
}
