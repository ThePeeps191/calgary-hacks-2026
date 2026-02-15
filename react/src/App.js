import "./App.css";
import { useState } from "react";
import { motion } from "framer-motion";

/* ── Background floating paths ── */
function FloatingPaths({ position }) {
  const paths = Array.from({ length: 36 }, (_, i) => ({
    id: i,
    d: `M-${380 - i * 5 * position} -${189 + i * 6}C-${
      380 - i * 5 * position
    } -${189 + i * 6} -${312 - i * 5 * position} ${216 - i * 6} ${
      152 - i * 5 * position
    } ${343 - i * 6}C${616 - i * 5 * position} ${470 - i * 6} ${
      684 - i * 5 * position
    } ${875 - i * 6} ${684 - i * 5 * position} ${875 - i * 6}`,
    width: 0.5 + i * 0.03,
  }));

  return (
    <div className="sf-paths-layer">
      <svg className="sf-paths-svg" viewBox="0 0 696 316" fill="none">
        {paths.map((path) => (
          <motion.path
            key={path.id}
            d={path.d}
            stroke="rgba(255,255,255,0.9)"
            strokeWidth={path.width}
            strokeOpacity={0.08 + path.id * 0.018}
            initial={{ pathLength: 0.3, opacity: 0.6 }}
            animate={{
              pathLength: 1,
              opacity: [0.3, 0.6, 0.3],
              pathOffset: [0, 1, 0],
            }}
            transition={{
              duration: 20 + (path.id % 7) * 3,
              repeat: Infinity,
              ease: "linear",
            }}
          />
        ))}
      </svg>
    </div>
  );
}

/* ── Bias helpers ── */
function getBiasStyle(score) {
  if (score <= 20)
    return { color: "#16a34a", label: "Minimal Bias", bg: "#f0fdf4" };
  if (score <= 40)
    return { color: "#65a30d", label: "Low Bias", bg: "#f7fee7" };
  if (score <= 60)
    return { color: "#ca8a04", label: "Moderate Bias", bg: "#fefce8" };
  if (score <= 80)
    return { color: "#ea580c", label: "High Bias", bg: "#fff7ed" };
  return { color: "#dc2626", label: "Extreme Bias", bg: "#fef2f2" };
}

function getDramaStyle(score) {
  if (score <= 20)
    return {
      color: "#0ea5e9",
      label: "Calm & Measured",
      bg: "#f0f9ff",
      icon: "😐",
    };
  if (score <= 40)
    return {
      color: "#6366f1",
      label: "Mildly Dramatic",
      bg: "#eef2ff",
      icon: "🤔",
    };
  if (score <= 60)
    return {
      color: "#f59e0b",
      label: "Emotionally Charged",
      bg: "#fffbeb",
      icon: "😤",
    };
  if (score <= 80)
    return {
      color: "#ef4444",
      label: "Highly Dramatic",
      bg: "#fef2f2",
      icon: "😡",
    };
  return {
    color: "#7c3aed",
    label: "Sensationalist",
    bg: "#f5f3ff",
    icon: "🔥",
  };
}

const HOW_IT_WORKS = [
  {
    icon: "🔗",
    step: "1",
    title: "Paste a URL",
    desc: "Drop in any news article link from any publication.",
  },
  {
    icon: "🔍",
    step: "2",
    title: "We Scrape & Analyze",
    desc: "Our tool extracts the text and runs AI-powered bias analysis.",
  },
  {
    icon: "📊",
    step: "3",
    title: "Get Your Report",
    desc: "Receive a bias score, unbiased summary, and full reasoning.",
  },
];

const INPUT_TABS = [
  { id: "url", label: "🔗 URL" },
  { id: "audio", label: "🎙 Audio" },
  { id: "video", label: "🎬 Video" },
];

/* ── Main App ── */
function App() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [activeInput, setActiveInput] = useState("url");
  const [audioFile, setAudioFile] = useState(null);
  const [videoFile, setVideoFile] = useState("url");
  const [currentParagraph, setCurrentParagraph] = useState(0);
  const [dramaIndex, setDramaIndex] = useState(null);
  const [dramaLoading, setDramaLoading] = useState(false);

  const fetchDramaIndex = async (text) => {
    if (!text) return;
    setDramaLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:5000/get-drama-index", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();
      if (data.status === "success" && data.drama_index != null) {
        setDramaIndex(data.drama_index[0]);
      }
    } catch (_) {
      // drama index is a bonus — don't surface errors for it
    } finally {
      setDramaLoading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!url.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);
    setDramaIndex(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/fetch-url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      const data = await response.json();
      console.log("Backend response:", data);
      setLoading(false);
      if (data.status === "ok") {
        setResult(data.data);
        fetchDramaIndex(data.data.summary || "");
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
    setDramaIndex(null);

    try {
      const formData = new FormData();
      formData.append("file", audioFile);
      const response = await fetch("http://127.0.0.1:5000/fetch-audio", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setLoading(false);
      if (data.status === "ok") {
        setResult(data.data);
        fetchDramaIndex(data.data.text || "");
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
      const response = await fetch("http://127.0.0.1:5000/fetch-video", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      const data = await response.json();
      console.log("Backend response:", data);
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

  const biasScore = result?.bias_score;
  const biasStyle = biasScore !== undefined ? getBiasStyle(biasScore) : null;

  return (
    <div className="sf-app">
      {/* ── Hero Header with flowing background paths ── */}
      <header className="sf-header">
        <FloatingPaths position={1} />
        <FloatingPaths position={-1} />
        <div className="sf-header-inner">
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, ease: "easeOut" }}
          >
            <div className="sf-logo">
              <span className="sf-logo-icon">⚖️</span>
              {"SpinFilter".split("").map((letter, i) => (
                <motion.span
                  key={i}
                  initial={{ y: 40, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{
                    delay: i * 0.045,
                    type: "spring",
                    stiffness: 150,
                    damping: 22,
                  }}
                  className="sf-logo-letter"
                >
                  {letter}
                </motion.span>
              ))}
            </div>
            <motion.p
              className="sf-tagline"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.65, duration: 0.6 }}
            >
              Cut through the spin. Detect media bias in seconds. Arrive at the
              truth.
            </motion.p>
          </motion.div>
        </div>
      </header>

      {/* ── Input Section ── */}
      <motion.section
        className="sf-search"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.5 }}
      >
        <h2 className="sf-search-title">Analyze Content</h2>
        <p className="sf-search-desc">
          Analyze news articles, audio clips, or videos for media bias.
        </p>

        {/* Tab selector */}
        <div className="sf-tabs">
          {INPUT_TABS.map((tab) => (
            <button
              key={tab.id}
              className={`sf-tab ${activeInput === tab.id ? "sf-tab-active" : ""}`}
              onClick={() => {
                setActiveInput(tab.id);
                setError("");
                setResult(null);
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* URL input */}
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

        {/* Audio input */}
        {activeInput === "audio" && (
          <div className="sf-input-row sf-file-row">
            <label className="sf-file-label">
              <span className="sf-file-icon">🎙</span>
              {audioFile ? audioFile.name : "Choose an audio file…"}
              <input
                type="file"
                accept="audio/*"
                onChange={(e) => setAudioFile(e.target.files[0])}
                disabled={loading}
                className="sf-file-hidden"
              />
            </label>
            <button
              className="sf-btn"
              onClick={handleAnalyzeAudio}
              disabled={loading || !audioFile}
            >
              {loading ? "Analyzing…" : "Analyze Audio"}
            </button>
          </div>
        )}

        {/* Video input */}
        {activeInput === "video" && (
          <div className="sf-input-row sf-file-row">
            <label className="sf-file-label">
              <span className="sf-file-icon">🎬</span>
              {videoFile ? videoFile.name : "Choose a video file…"}
              <input
                type="url"
                placeholder="https://youtube.com/…"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                onKeyDown={(e) =>
                  e.key === "Enter" &&
                  !loading &&
                  url.trim() &&
                  handleAnalyzeVideo()
                }
                disabled={loading}
                className="sf-file-hidden"
              />
            </label>
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
      </motion.section>

      {/* ── How It Works (shown before any result) ── */}
      {!result && !loading && (
        <motion.section
          className="sf-how"
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.5 }}
        >
          <h3 className="sf-how-title">How It Works</h3>
          <div className="sf-how-grid">
            {HOW_IT_WORKS.map((item, i) => (
              <motion.div
                className="sf-how-card"
                key={i}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 + i * 0.12, duration: 0.4 }}
              >
                <div className="sf-how-icon">{item.icon}</div>
                <div className="sf-how-step">Step {item.step}</div>
                <div className="sf-how-heading">{item.title}</div>
                <p className="sf-how-desc">{item.desc}</p>
              </motion.div>
            ))}
          </div>
        </motion.section>
      )}

      {/* ── Loading ── */}
      {loading && (
        <div className="sf-loading">
          <div className="sf-spinner" />
          <p>Fetching and analyzing content…</p>
        </div>
      )}

      {/* ── Results ── */}
      {result && !loading && (
        <motion.div
          className="sf-results"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          {/* Bias Score */}
          <div
            className="sf-card sf-card-bias"
            style={
              biasStyle ? { borderTop: `4px solid ${biasStyle.color}` } : {}
            }
          >
            <h3 className="sf-card-label">Bias Score</h3>
            {biasStyle ? (
              <>
                <div className="sf-bias-row">
                  <div
                    className="sf-bias-number"
                    style={{ color: biasStyle.color }}
                  >
                    {biasScore}
                    <span className="sf-bias-denom">/100</span>
                  </div>
                  <div
                    className="sf-bias-badge"
                    style={{ background: biasStyle.bg, color: biasStyle.color }}
                  >
                    {biasStyle.label}
                  </div>
                </div>
                <div className="sf-bar-track">
                  <motion.div
                    className="sf-bar-fill"
                    style={{ background: biasStyle.color }}
                    initial={{ width: 0 }}
                    animate={{ width: `${biasScore}%` }}
                    transition={{ duration: 1, ease: "easeOut" }}
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

          {/* Drama Index */}
          {(dramaIndex != null || dramaLoading) && (
            <motion.div
              className="sf-card sf-card-drama"
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              style={
                dramaIndex != null
                  ? {
                      borderTop: `4px solid ${getDramaStyle(dramaIndex).color}`,
                    }
                  : {}
              }
            >
              <h3 className="sf-card-label">Drama Index</h3>
              {dramaLoading ? (
                <div className="sf-drama-loading">
                  <div className="sf-spinner sf-spinner-sm" />
                  <span>Calculating emotional intensity…</span>
                </div>
              ) : (
                <>
                  <div className="sf-bias-row">
                    <div
                      className="sf-bias-number"
                      style={{ color: getDramaStyle(dramaIndex).color }}
                    >
                      {dramaIndex}
                      <span className="sf-bias-denom">/100</span>
                    </div>
                    <div className="sf-drama-badge-group">
                      <span className="sf-drama-icon">
                        {getDramaStyle(dramaIndex).icon}
                      </span>
                      <div
                        className="sf-bias-badge"
                        style={{
                          background: getDramaStyle(dramaIndex).bg,
                          color: getDramaStyle(dramaIndex).color,
                        }}
                      >
                        {getDramaStyle(dramaIndex).label}
                      </div>
                    </div>
                  </div>
                  <div className="sf-bar-track">
                    <motion.div
                      className="sf-bar-fill"
                      style={{ background: getDramaStyle(dramaIndex).color }}
                      initial={{ width: 0 }}
                      animate={{ width: `${dramaIndex}%` }}
                      transition={{ duration: 1, ease: "easeOut" }}
                    />
                  </div>
                  <div className="sf-bar-scale">
                    <span>1 — Calm</span>
                    <span>100 — Sensationalist</span>
                  </div>
                  <p className="sf-drama-desc">
                    Measures emotional intensity and use of manipulative
                    language — independent of political lean.
                  </p>
                </>
              )}
            </motion.div>
          )}

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

          {/* Summary / Transcription */}
          {result.summary && (
            <div className="sf-card">
              <h3 className="sf-card-label">
                {activeInput === "audio"
                  ? "Transcribed Text"
                  : "Unbiased Summary"}
              </h3>
              <p className="sf-summary-text">{result.summary}</p>
            </div>
          )}

          {/* Bias Reasons */}
          {result.reasons?.length > 0 && (
            <div className="sf-card">
              <h3 className="sf-card-label">Why It's Biased</h3>
              <ul className="sf-reasons-list">
                {result.reasons.map((reason, i) => (
                  <motion.li
                    key={i}
                    initial={{ opacity: 0, x: -8 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.08 }}
                  >
                    {reason}
                  </motion.li>
                ))}
              </ul>
            </div>
          )}

          {/* Paragraph‑level Bias Analysis */}
          {result.paragraphs?.length > 0 && (
            <div className="sf-card">
              <h3 className="sf-card-label">Paragraph Analysis</h3>

              <div className="sf-paragraphs-full">
                {/* Column labels at the top */}
                <div className="sf-para-labels-top">
                  <span className="sf-label-original">Original / Changed</span>
                  <span className="sf-label-unbiased">
                    Unbiased / Unchanged
                  </span>
                </div>

                {/* Loop through all paragraphs */}
                {result.paragraphs.map((para, idx) => (
                  <div key={idx} className="sf-para-container">
                    <div
                      className={`sf-para-row ${
                        para.bias_score ? "sf-para-biased" : "sf-para-clean"
                      }`}
                    >
                      {/* Original paragraph */}
                      <div className="sf-para-original">
                        <p>{para.text}</p>
                      </div>

                      {/* Unbiased paragraph */}
                      <div className="sf-para-unbiased">
                        <p>{para.unbiased_replacement || para.text}</p>
                      </div>
                    </div>

                    {/* Bias reason below the paragraph */}
                    {para.bias_score && para.reason_biased && (
                      <div className="sf-para-reason">
                        <span className="sf-para-tag">Reason for bias:</span>
                        <p>{para.reason_biased}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Keywords */}
          {result.keywords?.length > 0 && (
            <div className="sf-card">
              <h3 className="sf-card-label">Keywords</h3>
              <div className="sf-keywords">
                {result.keywords.map((k, i) => (
                  <motion.span
                    className="sf-keyword"
                    key={i}
                    initial={{ opacity: 0, scale: 0.85 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: i * 0.04 }}
                  >
                    {k}
                  </motion.span>
                ))}
              </div>
            </div>
          )}
        </motion.div>
      )}

      {/* ── Footer ── */}
      <footer className="sf-footer">
        <span className="sf-footer-logo">⚖️ SpinFilter</span>
        <span className="sf-footer-sep">·</span>
        Calgary Hacks 2026
        <span className="sf-footer-sep">·</span>
        Bias detection powered by AI
      </footer>
    </div>
  );
}

export default App;
