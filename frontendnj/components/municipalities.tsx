"use client";

import * as React from "react";
import { Check, ChevronsUpDown } from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { fetchMunicipalities } from "../lib/queries";

const m = [
  {
    value: "next.js",
    label: "Next.js",
  },
  {
    value: "sveltekit",
    label: "SvelteKit",
  },
  {
    value: "nuxt.js",
    label: "Nuxt.js",
  },
  {
    value: "remix",
    label: "Remix",
  },
  {
    value: "astro",
    label: "Astro",
  },
];

export type Bbox = {
  xmin: number;
  ymin: number;
  xmax: number;
  ymax: number;
};

export type Municipality = {
  codiMunicipi: string;
  nomMunicipi: string;
  bbox: Bbox;
};

type MunicipalitiesProps = {
  onSelectMunicipality: (municipality: Municipality) => void;
};

export function Municipalities({ onSelectMunicipality }: MunicipalitiesProps) {
  const [open, setOpen] = React.useState(false);
  const [value, setValue] = React.useState("");
  const [municipalities, setMunicipalities] = React.useState<Municipality[]>(
    []
  );

  React.useEffect(() => {
    fetchMunicipalities().then((data) => {
      setMunicipalities(data);
    });
  }, []);

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-100 justify-between"
        >
          {value
            ? municipalities.find(
                (municipality) => municipality.codiMunicipi === value
              )?.nomMunicipi
            : "Selecciona una municipalitat..."}
          <ChevronsUpDown className="opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0">
        <Command>
          <CommandInput placeholder="Buscar municipalitat..." className="h-9" />
          <CommandList>
            <CommandEmpty>No s'ha trobat cap municipalitat</CommandEmpty>
            <CommandGroup>
              {municipalities.map((municipality) => (
                <CommandItem
                  key={municipality.codiMunicipi}
                  value={municipality.nomMunicipi}
                  onSelect={(currentValue) => {
                    /* Find the value of the selected municipality */
                    const selectedMunicipality = municipalities.find(
                      (mun) => mun.nomMunicipi === currentValue
                    );

                    if (!selectedMunicipality) {
                      return;
                    }
                    setValue(
                      selectedMunicipality.codiMunicipi === value
                        ? ""
                        : selectedMunicipality.codiMunicipi
                    );
                    setOpen(false);
                    onSelectMunicipality(selectedMunicipality);
                  }}
                >
                  {municipality.nomMunicipi}
                  <Check
                    className={cn(
                      "ml-auto",
                      value === municipality.codiMunicipi
                        ? "opacity-100"
                        : "opacity-0"
                    )}
                  />
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
