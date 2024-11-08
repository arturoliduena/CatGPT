import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import "./App.css";
import { Form } from './components/Form';
const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
    
     <Form/>
    </QueryClientProvider>
  );
}

export default App;
