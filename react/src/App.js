import logo from "./logo.svg";
import "./App.css";
import { useState } from "react";

function App() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  const fetchContent = async () => {
    if (!url.trim()) {
      setError("Please enter a URL");
      return;
    }

    setLoading(true);
    setError("");
    setResult("");

    try {
      const response = await fetch("http://127.0.0.1:5000/fetch-url", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();
      setLoading(false);

      if (data.status === "ok") {
        setResult(data.data.text);
      } else {
        setError(data.message || "Error fetching content");
      }
    } catch (err) {
      setLoading(false);
      setError("Network error: " + err.message);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") fetchContent();
  };

  return (
    <div style={styles.body}>
      <div style={styles.container}>
        <h1 style={styles.title}>📰 URL Content Fetcher</h1>

        <div style={styles.inputGroup}>
          <input
            type="text"
            placeholder="Paste your URL here..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onKeyPress={handleKeyPress}
            style={styles.input}
          />
          <button
            onClick={fetchContent}
            style={styles.button}
            disabled={loading}
          >
            Fetch
          </button>
        </div>

        {loading && (
          <div style={styles.loading}>
            <div style={styles.spinner}></div>
            <p>Loading...</p>
          </div>
        )}

        {error && <div style={styles.error}>{error}</div>}

        {result && (
          <div style={styles.result}>
            <h2>Article Content</h2>
            <p>{result}</p>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  body: {
    fontFamily: "Arial, sans-serif",
    background: "linear-gradient(135deg, #48e17d 0%, #4bd6c6 100%)",
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    padding: "20px",
  },
  container: {
    background: "white",
    borderRadius: "10px",
    boxShadow: "0 10px 40px rgba(0,0,0,0.2)",
    padding: "40px",
    maxWidth: "600px",
    width: "100%",
  },
  title: {
    color: "#333",
    marginBottom: "30px",
    textAlign: "center",
  },
  inputGroup: {
    display: "flex",
    gap: "10px",
    marginBottom: "20px",
  },
  input: {
    flex: 1,
    padding: "12px",
    border: "2px solid #ddd",
    borderRadius: "5px",
    fontSize: "14px",
    outline: "none",
  },
  button: {
    padding: "12px 30px",
    background: "#667eea",
    color: "white",
    border: "none",
    borderRadius: "5px",
    fontSize: "14px",
    cursor: "pointer",
    transition: "background 0.3s",
  },
  loading: {
    textAlign: "center",
    margin: "30px 0",
  },
  spinner: {
    border: "4px solid #f3f3f3",
    borderTop: "4px solid #667eea",
    borderRadius: "50%",
    width: "40px",
    height: "40px",
    animation: "spin 1s linear infinite",
    margin: "0 auto",
  },
  result: {
    marginTop: "30px",
    padding: "20px",
    background: "#f9f9f9",
    borderRadius: "5px",
    maxHeight: "400px",
    overflowY: "auto",
  },
  error: {
    color: "#e74c3c",
    padding: "15px",
    background: "#fdeaea",
    borderRadius: "5px",
    marginTop: "20px",
  },
};

export default App;
