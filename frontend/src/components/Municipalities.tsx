import { useQuery } from "@tanstack/react-query"
import {fetchMunicipalities} from "../queries"

export const Municipalities = ()=>{
    const {data,status} = useQuery({ queryKey: ['municipalities'], queryFn: fetchMunicipalities })
    console.log(data, status);
    return <div className="text">Hola</div>
}