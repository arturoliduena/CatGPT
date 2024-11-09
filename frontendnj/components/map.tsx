import { LegacyRef, useEffect, useRef, useState } from "react";
import { MapContainer, TileLayer, Marker, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-defaulticon-compatibility";
import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css";
import { FloodableZone } from "@/lib/queries";

const MapComponent = ({
  bounds,floodableZones
}: {
  bounds: [[number, number], [number, number]];
  floodableZones:FloodableZone[]
}) => {
  const map = useMap();
  useEffect(() => {
    map.fitBounds(bounds);
  }, [bounds, map]);

  useEffect(()=>{
    if ( floodableZones.length > 0) {
      map.eachLayer((layer: any) => {
        if (layer instanceof L.GeoJSON) {
          map.removeLayer(layer);
        }
       });

       floodableZones.forEach((zone) => {
        const geoJsonData = JSON.parse(zone.geom); 
        console.log("----", geoJsonData)
        L.geoJSON(geoJsonData).addTo(map);
      });
    }

  }, [floodableZones, map])

  return null;
};



export default function MyMap({
  initialBounds, floodableZones=[]
}: {
  initialBounds: [number, number][];floodableZones:FloodableZone[]
}) {
  const [bounds, setBounds] = useState<[number, number][]>(initialBounds);
  useEffect(() => {
    setBounds(initialBounds);
  }, [initialBounds]);


  
  return (
    <MapContainer bounds={bounds} style={{ height: "100%", width: "100%" }} >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      <MapComponent bounds={bounds} floodableZones={floodableZones}/>
    </MapContainer>
  );
}
