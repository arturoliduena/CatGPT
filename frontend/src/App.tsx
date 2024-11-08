import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Municipalities } from './components/Municipalities';
const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Municipalities/>
      </QueryClientProvider>
  );
}

export default App;
