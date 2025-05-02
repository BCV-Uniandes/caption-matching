import "./App.css";
import { Navbar } from "./components/navigation/Navbar";
import { Dataset } from "./components/dataset/Dataset";

function App() {
  return (
    <div>
        <Navbar />
        <Dataset />
    </div>
  );
}

export default App;