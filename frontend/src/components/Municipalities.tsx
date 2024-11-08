import { useQuery } from "@tanstack/react-query"
import {fetchMunicipalities} from "../queries"
import { Dropdown } from "flowbite-react";
import { useState } from "react";

export const Municipalities = ({onChange}:{onChange: (val:string)=>void})=>{
    const {data} = useQuery<[string, string][]>({ queryKey: ['municipalities'], queryFn: fetchMunicipalities })
    
    const [selectedMunicipality, setSelectedMunicipality] =useState<string>()

    const selectedName = data?.find(([id]) => id === selectedMunicipality)?.[1]

    return  <Dropdown 
    label={ selectedName||"Selecciona el municipi"} 
    dismissOnClick={true}
>
    {data?.map(([id, municipality]) => (
        <Dropdown.Item 
            key={id} 
            value={id}
            onClick={() => {setSelectedMunicipality(id); onChange(id)}}
        >
            {municipality}
        </Dropdown.Item>
    ))}
</Dropdown>
}