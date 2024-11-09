import { LegacyRef, useEffect, useRef, useState } from "react";
import { MapContainer, TileLayer, Marker, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-defaulticon-compatibility";
import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css";
import { FloodableZone, POI } from "@/lib/queries";

const MapComponent = ({
  bounds,floodableZones, poi
}: {
  bounds: [[number, number], [number, number]];
  floodableZones:FloodableZone[],
  poi: POI[]
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
        L.geoJSON(geoJsonData).addTo(map);
      });
    }

  }, [floodableZones, map])

  useEffect(()=>{
    if ( poi.length > 0) {
      map.eachLayer((layer: any) => {
        if (layer instanceof L.CircleMarker) {
          map.removeLayer(layer);
        }
       });

       poi.forEach((zone) => {
        const color = zone.floodable ? "red" : "green";
        L.circleMarker([zone.lat, zone.lon], {
          color: color,
          fillColor: color,
          radius: 8, // Size of the CircleMarker
          fillOpacity: 0.6,
        })
        .addTo(map)
        .bindPopup(`${zone.amenity} <b>${zone.name}</b><br>inundable: ${zone.floodable}`);
      });
    }

  }, [poi, map])


  return null;
};



export default function MyMap({
  initialBounds, floodableZones=[], poi=[]
}: {
  initialBounds: [number, number][];floodableZones:FloodableZone[], poi:POI[]
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
      <MapComponent bounds={bounds} floodableZones={floodableZones} poi={poi}/>
    </MapContainer>
  );
}
