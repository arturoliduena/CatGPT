import { Button, TextInput } from "flowbite-react"
import { useState } from "react"
import { Municipalities } from "./Municipalities"
import { useMutation } from "@tanstack/react-query"

interface FormData {
    municipality: string,
     input: string
}
export const Form = () => {
    const [formData, setFormData] = useState<FormData>({municipality: "", input: ""})
    
    const mutation = useMutation({
        mutationFn: async (data: FormData) => {
          return await fetch('http://localhost:8000/forecast-summary',{
            body: JSON.stringify({municipe_code: data.municipality, alert_message: data.input}),
            method: "POST" 
          })
        },
      })

      
    return <div> 
        <Municipalities onChange={val=>setFormData(cur=>({...cur, municipality: val}))}/>
        <TextInput id="small" type="text" sizing="lg" onChange={val=>setFormData(cur=>({...cur, input: val.currentTarget?.value??""}))}/>
      <Button onClick={()=>mutation.mutate(formData)}>Default</Button>
      </div>
}