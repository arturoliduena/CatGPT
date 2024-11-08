export const fetchMunicipalities = async () => {
  const res = await fetch("http://localhost:8000/municipalities");
  console.log("HOLA");
  return res;
};
