import "./App.css";
import { useState } from "react";

function getBiasStyle(score) {
  if (score <= 20) return { color: "#16a34a", label: "Minimal Bias" };
  if (score <= 40) return { color: "#65a30d", label: "Low Bias" };
  if (score <= 60) return { color: "#ca8a04", label: "Moderate Bias" };
  if (score <= 80) return { color: "#ea580c", label: "High Bias" };
  return { color: "#dc2626", label: "Extreme Bias" };
}

function App() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [activeInput, setActiveInput] = useState("url"); // which input to show
  const [audioFile, setAudioFile] = useState(null);
  const [videoFile, setVideoFile] = useState(null);

  const handleAnalyze = async () => {
    if (!url.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/fetch-url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();
      setLoading(false);

      if (data.status === "ok") {
        setResult(data.data);
      } else {
        setError(data.message || "Error fetching content.");
      }
    } catch (err) {
      setLoading(false);
      setError("Could not reach the server. Is the backend running?");
    }
  };

  const handleAnalyzeAudio = async () => {
    if (!audioFile) return;
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", audioFile);

      const response = await fetch("http://127.0.0.1:5000/fetch-audio", {
        method: "POST",
        body: formData, // no JSON, we send FormData for file uploads
      });

      const data = await response.json();
      setLoading(false);

      if (data.status === "ok") {
        setResult(data.data);
      } else {
        setError(data.message || "Error analyzing audio.");
      }
    } catch (err) {
      setLoading(false);
      setError("Could not reach the server. Is the backend running?");
    }
  };

  const handleAnalyzeVideo = async () => {
    if (!videoFile) return;
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", videoFile);

      const response = await fetch("http://127.0.0.1:5000/fetch-video", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setLoading(false);

      if (data.status === "ok") {
        setResult(data.data);
      } else {
        setError(data.message || "Error analyzing video.");
      }
    } catch (err) {
      setLoading(false);
      setError("Could not reach the server. Is the backend running?");
    }
  };

  const biasScore = result?.bias_score;
  const biasStyle = biasScore !== undefined ? getBiasStyle(biasScore) : null;

  return (
    <div className="sf-app">
      {/* ── Header ── */}
      <header className="sf-header">
        <div className="sf-header-inner">
          <div className="sf-logo">
            <span className="sf-logo-icon">⚖️</span>
            SpinFilter
          </div>
          <p className="sf-tagline">
            Cut through the spin. Detect media bias in seconds.
          </p>
        </div>
      </header>

      {/* ── Input Selector ── */}
      <section className="sf-search">
        <h2 className="sf-search-title">Analyze Content</h2>
        <p className="sf-search-desc">
          Choose a content type to analyze: URL, audio, or video.
        </p>

        {/* Three buttons side by side */}
        <div className="sf-button-row">
          <button className="sf-btn" onClick={() => setActiveInput("url")}>
            URL
          </button>
          <button className="sf-btn" onClick={() => setActiveInput("audio")}>
            Audio
          </button>
          <button className="sf-btn" onClick={() => setActiveInput("video")}>
            Video
          </button>
        </div>

        {/* Conditional rendering of input areas */}
        {activeInput === "url" && (
          <div className="sf-input-row">
            <input
              type="url"
              placeholder="https://example.com/news-article…"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              onKeyDown={(e) =>
                e.key === "Enter" && !loading && url.trim() && handleAnalyze()
              }
              disabled={loading}
              className="sf-url-input"
            />
            <button
              className="sf-btn"
              onClick={handleAnalyze}
              disabled={loading || !url.trim()}
            >
              {loading ? "Analyzing…" : "Analyze"}
            </button>
          </div>
        )}

        {activeInput === "audio" && (
          <div className="sf-input-row">
            <input
              type="file"
              accept="audio/*"
              onChange={(e) => setAudioFile(e.target.files[0])}
              disabled={loading}
            />
            <button
              className="sf-btn"
              onClick={handleAnalyzeAudio}
              disabled={loading || !audioFile}
            >
              {loading ? "Analyzing…" : "Analyze Audio"}
            </button>
          </div>
        )}

        {activeInput === "video" && (
          <div className="sf-input-row">
            <input
              type="file"
              accept="video/*"
              onChange={(e) => setVideoFile(e.target.files[0])}
              disabled={loading}
            />
            <button
              className="sf-btn"
              onClick={handleAnalyzeVideo}
              disabled={loading || !videoFile}
            >
              {loading ? "Analyzing…" : "Analyze Video"}
            </button>
          </div>
        )}

        {error && <div className="sf-error">{error}</div>}
      </section>

      {/* ── Loading ── */}
      {loading && (
        <div className="sf-loading">
          <div className="sf-spinner" />
          <p>Fetching and analyzing article…</p>
        </div>
      )}

      {/* ── Results ── */}
      {result && !loading && (
        <div className="sf-results">
          {/* Bias Score */}
          <div className="sf-card sf-card-bias">
            <h3 className="sf-card-label">Bias Score</h3>
            {biasStyle ? (
              <>
                <div
                  className="sf-bias-number"
                  style={{ color: biasStyle.color }}
                >
                  {biasScore}
                  <span className="sf-bias-denom">/100</span>
                </div>
                <div
                  className="sf-bias-verdict"
                  style={{ color: biasStyle.color }}
                >
                  {biasStyle.label}
                </div>
                <div className="sf-bar-track">
                  <div
                    className="sf-bar-fill"
                    style={{
                      width: `${biasScore}%`,
                      background: biasStyle.color,
                    }}
                  />
                </div>
                <div className="sf-bar-scale">
                  <span>0 — Unbiased</span>
                  <span>100 — Extremely Biased</span>
                </div>
              </>
            ) : (
              <p className="sf-bias-pending">
                Bias analysis is pending — the backend is still working on it.
              </p>
            )}
          </div>

          {/* Article Info */}
          <div className="sf-card">
            <h3 className="sf-card-label">Article Info</h3>
            {result.top_image && (
              <img
                src={result.top_image}
                alt="Article"
                className="sf-article-img"
              />
            )}
            <div className="sf-meta-grid">
              {result.authors?.length > 0 && (
                <div className="sf-meta-item">
                  <label>Authors</label>
                  <span>{result.authors.join(", ")}</span>
                </div>
              )}
              {result.date && (
                <div className="sf-meta-item">
                  <label>Published</label>
                  <span>{result.date}</span>
                </div>
              )}
            </div>
          </div>

          {/* Summary */}
          {result.summary && (
            <div className="sf-card">
              <h3 className="sf-card-label">Unbiased Summary</h3>
              <p className="sf-summary-text">{result.summary}</p>
            </div>
          )}

          {/* Bias Reasons */}
          {result.reasons?.length > 0 && (
            <div className="sf-card">
              <h3 className="sf-card-label">Why It's Biased</h3>
              <ul className="sf-reasons-list">
                {result.reasons.map((reason, i) => (
                  <li key={i}>{reason}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Keywords */}
          {result.keywords?.length > 0 && (
            <div className="sf-card">
              <h3 className="sf-card-label">Keywords</h3>
              <div className="sf-keywords">
                {result.keywords.map((k, i) => (
                  <span className="sf-keyword" key={i}>
                    {k}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* ── Footer ── */}
      <footer className="sf-footer">
        <span>⚖️ SpinFilter</span> — Calgary Hacks 2026
      </footer>
    </div>
  );
}

export default App;
