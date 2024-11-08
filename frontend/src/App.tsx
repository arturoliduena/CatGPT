import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Municipalities } from './components/Municipalities';
import "./App.css";
const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
    
      <Municipalities/>
    </QueryClientProvider>
  );
}

export default App;
