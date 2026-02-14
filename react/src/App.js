import logo from "./logo.svg";
import "./App.css";
import { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [output, setOutput] = useState("");

  const handleSend = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/api", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });

      const data = await res.json();
      setOutput(data.result);
    } catch (err) {
      console.error("Error:", err);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <p>Please put your text</p>
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Text"
        />
        <button onClick={handleSend}>Check</button>

        {output && (
          <p>
            <strong>Response:</strong> {output}
          </p>
        )}
      </header>
    </div>
  );
}

export default App;
