import { useState, useEffect, useRef } from "react";

const COMPANIES = [
  { name: "Reliance", color: "#00d4aa" },
  { name: "TCS", color: "#3b82f6" },
  { name: "HDFC Bank", color: "#8b5cf6" },
  { name: "Infosys", color: "#f59e0b" },
  { name: "ICICI Bank", color: "#ec4899" },
];

const PLACEHOLDER_QUERIES = [
  "What was the revenue of Reliance in 2024?",
  "Compare HDFC Bank net profit with ICICI Bank in 2023",
  "Show EPS trend for TCS over last 3 years",
  "What is the P/E ratio of Infosys?",
  "Which company had better operating cash flow in 2024?",
];

const SAMPLE_INSIGHTS = {
  Reliance: {
    title: "Reliance Industries Limited — Performance Summary",
    body: [
      "Reliance Industries Limited delivered a robust financial performance in fiscal year 2024, cementing its position as India's most valuable conglomerate. Consolidated revenue from operations reached ₹9,73,420 crore, reflecting a year-on-year growth of 6.2% driven by its Retail and Jio Platforms segments.",
      "Net profit attributable to shareholders stood at ₹69,621 crore, marking an 8.4% increase. EBITDA expanded to ₹1,75,380 crore with margins improving to 18.0%. The Jio Platforms segment recorded subscriber additions of 4.2 crore, bringing total user base to 48.9 crore with ARPU improving to ₹181.7 per month.",
      "Reliance Retail maintained its dominance with 18,774 stores and gross revenue of ₹3,12,394 crore. The Oil-to-Chemicals (O2C) segment remained resilient despite margin headwinds in global refining spreads. Capital expenditure stood at ₹1,59,299 crore, reflecting continued investment in 5G rollout and new energy initiatives.",
    ],
    metrics: [
      { label: "Revenue", value: "₹9,73,420 Cr", change: "+6.2%", positive: true },
      { label: "Net Profit", value: "₹69,621 Cr", change: "+8.4%", positive: true },
      { label: "EBITDA", value: "₹1,75,380 Cr", change: "+9.1%", positive: true },
      { label: "EPS", value: "₹103.4", change: "+7.9%", positive: true },
    ],
  },
  TCS: {
    title: "Tata Consultancy Services — Performance Summary",
    body: [
      "Tata Consultancy Services reported steady performance in FY2024 against a challenging global macro environment. Total revenue reached $29.1 billion, growing 8.2% in constant currency terms, with the North America vertical contributing 53% of total revenue.",
      "Operating margin held firm at 24.6%, reflecting disciplined cost management and efficient utilisation of its 6,02,110-strong workforce. Net income grew 8.9% to ₹46,099 crore. The BFSI vertical reported modest growth of 5.1%, while Manufacturing and Life Sciences outperformed at 12.3% and 10.8% respectively.",
      "Total Contract Value (TCV) of deal wins for the year stood at $42.7 billion, with a robust pipeline indicating resilience in demand for digital transformation. The company returned ₹52,452 crore to shareholders through dividends and buybacks.",
    ],
    metrics: [
      { label: "Revenue", value: "$29.1 Bn", change: "+8.2%", positive: true },
      { label: "Net Profit", value: "₹46,099 Cr", change: "+8.9%", positive: true },
      { label: "Op. Margin", value: "24.6%", change: "+0.3pp", positive: true },
      { label: "TCV Wins", value: "$42.7 Bn", change: "+11.2%", positive: true },
    ],
  },
  "HDFC Bank": {
    title: "HDFC Bank Limited — Performance Summary",
    body: [
      "HDFC Bank delivered a landmark year in FY2024, its first full fiscal year as a merged entity following the amalgamation with HDFC Limited. Net Interest Income (NII) grew to ₹89,639 crore, supported by an expanded balance sheet. Net Profit stood at ₹60,812 crore, rising 37.1% year-on-year.",
      "Gross advances grew 55.4% to ₹25.08 lakh crore, with retail and commercial segments leading momentum. The CASA ratio moderated to 38.2% as the bank focused on integrating the mortgage portfolio. Gross NPA ratio remained well-controlled at 1.24%, reflecting best-in-class credit underwriting standards.",
      "Capital adequacy ratio stood at 18.8% (Tier-1: 17.2%), providing a strong buffer for continued loan growth. The bank's digital platform processed over 50 crore transactions per month, underlining its technology-first approach.",
    ],
    metrics: [
      { label: "NII", value: "₹89,639 Cr", change: "+24.5%", positive: true },
      { label: "Net Profit", value: "₹60,812 Cr", change: "+37.1%", positive: true },
      { label: "Gross NPA", value: "1.24%", change: "-0.12pp", positive: true },
      { label: "CASA Ratio", value: "38.2%", change: "-2.1pp", positive: false },
    ],
  },
  Infosys: {
    title: "Infosys Limited — Performance Summary",
    body: [
      "Infosys navigated a cautious demand environment in FY2024, reporting revenue of $18.56 billion — growth of 1.4% in constant currency, reflecting softness in BFSI and Hi-Tech verticals amid client discretionary spending cuts. Operating margins improved to 20.7%, benefiting from Project Maximus efficiency initiatives.",
      "Net profit grew 8.9% in rupee terms to ₹26,248 crore, aided by a favourable effective tax rate and forex gains. Large deal wins remained healthy at $17.7 billion for the year, with a refreshed focus on generative AI-led transformation engagements.",
      "Free cash flow conversion was robust at 115% of net profit. The board approved a final dividend of ₹20 per share, with total capital return for the year at ₹22,754 crore including a buyback of ₹9,300 crore.",
    ],
    metrics: [
      { label: "Revenue", value: "$18.56 Bn", change: "+1.4%", positive: true },
      { label: "Net Profit", value: "₹26,248 Cr", change: "+8.9%", positive: true },
      { label: "Op. Margin", value: "20.7%", change: "+0.6pp", positive: true },
      { label: "Large Deals", value: "$17.7 Bn", change: "+2.1%", positive: true },
    ],
  },
  "ICICI Bank": {
    title: "ICICI Bank Limited — Performance Summary",
    body: [
      "ICICI Bank emerged as a standout performer in the Indian banking sector in FY2024, reporting Net Interest Income of ₹71,492 crore, a growth of 16.9% year-on-year. Core operating profit rose 15.4% to ₹55,628 crore, driven by strong credit growth and improving fee income traction.",
      "Net Profit surged 28.5% to ₹40,888 crore — one of the highest absolute profit additions in Indian banking history. The retail and SME loan book expanded 20.1%, while the corporate book grew steadily at 9.4%. Asset quality showed continued improvement with Gross NPA declining to 2.16%.",
      "Return on Assets improved to 2.30% and Return on Equity reached 18.5%, both above the bank's own guidance thresholds. Digital channels accounted for over 88% of all transactions, and iMobile Pay garnered over 1.1 crore activations from non-ICICI Bank customers.",
    ],
    metrics: [
      { label: "NII", value: "₹71,492 Cr", change: "+16.9%", positive: true },
      { label: "Net Profit", value: "₹40,888 Cr", change: "+28.5%", positive: true },
      { label: "Gross NPA", value: "2.16%", change: "-0.74pp", positive: true },
      { label: "RoE", value: "18.5%", change: "+2.1pp", positive: true },
    ],
  },
};

/* ── Animated typing placeholder ── */
function TypingPlaceholder() {
  const [idx, setIdx] = useState(0);
  const [text, setText] = useState("");
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const current = PLACEHOLDER_QUERIES[idx];
    const timeout = setTimeout(() => {
      if (!deleting && text.length < current.length) {
        setText(current.slice(0, text.length + 1));
      } else if (!deleting && text.length === current.length) {
        setTimeout(() => setDeleting(true), 2000);
      } else if (deleting && text.length > 0) {
        setText(text.slice(0, -1));
      } else {
        setDeleting(false);
        setIdx((p) => (p + 1) % PLACEHOLDER_QUERIES.length);
      }
    }, deleting ? 20 : 48);
    return () => clearTimeout(timeout);
  }, [text, deleting, idx]);

  return (
    <span style={{ color: "rgba(255,255,255,0.25)", pointerEvents: "none", userSelect: "none" }}>
      {text}
      <span style={{
        display: "inline-block", width: 2, height: "1em",
        background: "#00d4aa", marginLeft: 2, verticalAlign: "text-bottom",
        animation: "blink 1s step-end infinite",
      }} />
    </span>
  );
}

/* ── Metric card ── */
function MetricCard({ label, value, change, positive, delay }) {
  return (
    <div style={{
      background: "rgba(255,255,255,0.04)",
      border: "1px solid rgba(255,255,255,0.08)",
      borderRadius: 12, padding: "18px 20px",
      animation: `fadeUp 0.4s ease ${delay}ms both`,
    }}>
      <div style={{
        fontFamily: "monospace", fontSize: 10, letterSpacing: "0.1em",
        color: "rgba(255,255,255,0.3)", textTransform: "uppercase", marginBottom: 8,
      }}>{label}</div>
      <div style={{
        fontWeight: 700, fontSize: 19, color: "#e8edf5",
        letterSpacing: "-0.02em", marginBottom: 4,
      }}>{value}</div>
      <div style={{
        fontFamily: "monospace", fontSize: 11,
        color: positive ? "#00d4aa" : "#f87171",
      }}>{change}</div>
    </div>
  );
}

/* ── Main App ── */
export default function Documind() {
  const [query, setQuery] = useState("");
  const [focused, setFocused] = useState(false);
  const [activeCompany, setActiveCompany] = useState(null);
  const [insight, setInsight] = useState(null);
  const [loading, setLoading] = useState(false);
  const inputRef = useRef(null);

  const runQuery = (q, companyName) => {
    setLoading(true);
    setInsight(null);
    setTimeout(() => {
      const matched = companyName
        ? SAMPLE_INSIGHTS[companyName]
        : COMPANIES.reduce((found, c) =>
            !found && q.toLowerCase().includes(c.name.toLowerCase())
              ? SAMPLE_INSIGHTS[c.name] : found, null);

      setInsight(matched || {
        title: "Financial Intelligence Result",
        body: [
          "Your query has been processed by Documind's NER and Intent Classification pipeline.",
          "Entities detected: The system identified relevant financial metrics, company references, and temporal markers. In a live environment, this section would display precise metric values, trend analysis, peer comparisons, and AI-generated narrative summaries derived from official filings and earnings transcripts.",
          "Documind understands complex financial language — from simple metric lookups to multi-entity comparative analyses — and returns structured, readable intelligence in plain English.",
        ],
        metrics: [],
      });
      setLoading(false);
    }, 900);
  };

  const handleCompanyClick = (company) => {
    const q = `Performance summary of ${company.name}`;
    setActiveCompany(company.name);
    setQuery(q);
    runQuery(q, company.name);
  };

  const handleSearch = () => {
    if (!query.trim()) return;
    const matched = COMPANIES.find((c) => query.toLowerCase().includes(c.name.toLowerCase()));
    setActiveCompany(matched ? matched.name : null);
    runQuery(query, matched ? matched.name : null);
  };

  return (
    <div style={{ minHeight: "100vh", background: "#080c14", color: "#e8edf5", position: "relative", overflowX: "hidden" }}>
      <style>{`
        @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
        @keyframes fadeUp { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
        @keyframes spin { to{transform:rotate(360deg)} }
        @keyframes shimmer { 0%{background-position:200% center} 100%{background-position:-200% center} }
        @keyframes orb1 { 0%,100%{transform:translate(0,0)} 50%{transform:translate(30px,-25px)} }
        @keyframes orb2 { 0%,100%{transform:translate(0,0)} 50%{transform:translate(-40px,20px)} }
        * { box-sizing: border-box; }
        .chip-btn { transition: all 0.2s ease; cursor: pointer; }
        .chip-btn:hover { transform: translateY(-2px); border-color: rgba(255,255,255,0.22) !important; color: rgba(255,255,255,0.75) !important; }
        .send-btn { transition: all 0.2s ease; cursor: pointer; }
        .send-btn:hover { background: rgba(0,212,170,0.18) !important; transform: scale(1.06); }
      `}</style>

      {/* Ambient orbs */}
      <div style={{ position: "fixed", inset: 0, overflow: "hidden", pointerEvents: "none", zIndex: 0 }}>
        <div style={{ position: "absolute", top: "5%", left: "10%", width: 480, height: 480, borderRadius: "50%", background: "radial-gradient(circle, rgba(0,212,170,0.07) 0%, transparent 70%)", animation: "orb1 20s ease-in-out infinite" }} />
        <div style={{ position: "absolute", bottom: "10%", right: "5%", width: 400, height: 400, borderRadius: "50%", background: "radial-gradient(circle, rgba(59,130,246,0.07) 0%, transparent 70%)", animation: "orb2 25s ease-in-out infinite" }} />
      </div>

      <div style={{ position: "relative", zIndex: 1, maxWidth: 860, margin: "0 auto", padding: "0 24px 80px" }}>

        {/* Header */}
        <header style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "26px 0 0", animation: "fadeUp 0.5s ease both" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div style={{ width: 34, height: 34, background: "rgba(0,212,170,0.1)", border: "1px solid rgba(0,212,170,0.25)", borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center" }}>
              <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
                <path d="M10 2L18 7V13L10 18L2 13V7L10 2Z" stroke="#00d4aa" strokeWidth="1.5" />
                <path d="M10 2V18M2 7L18 13M18 7L2 13" stroke="#00d4aa" strokeWidth="0.7" opacity="0.4" />
              </svg>
            </div>
            <span style={{ fontWeight: 700, fontSize: 20, letterSpacing: "-0.03em", background: "linear-gradient(135deg,#e8edf5,rgba(232,237,245,0.5))", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
              Documind
            </span>
          </div>
          <span style={{ fontFamily: "monospace", fontSize: 10, letterSpacing: "0.09em", color: "#00d4aa", background: "rgba(0,212,170,0.1)", border: "1px solid rgba(0,212,170,0.2)", borderRadius: 4, padding: "3px 9px" }}>
            BETA
          </span>
        </header>

        {/* Hero */}
        <section style={{ padding: "64px 0 40px", animation: "fadeUp 0.5s ease 0.1s both" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 20 }}>
            <div style={{ width: 6, height: 6, borderRadius: "50%", background: "#00d4aa", boxShadow: "0 0 8px #00d4aa" }} />
            <span style={{ fontFamily: "monospace", fontSize: 11, letterSpacing: "0.12em", color: "rgba(232,237,245,0.35)", textTransform: "uppercase" }}>
              AI-Powered Financial Intelligence
            </span>
          </div>
          <h1 style={{ fontWeight: 800, fontSize: "clamp(32px,5vw,54px)", lineHeight: 1.07, letterSpacing: "-0.04em", color: "#e8edf5", marginBottom: 16 }}>
            Ask anything about{" "}
            <span style={{ background: "linear-gradient(135deg,#00d4aa,#3b82f6,#8b5cf6)", backgroundSize: "200%", animation: "shimmer 4s linear infinite", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
              financial markets
            </span>
          </h1>
          <p style={{ fontWeight: 300, fontSize: 15, lineHeight: 1.75, color: "rgba(232,237,245,0.36)" }}>
            Natural language queries. Instant structured insights.<br />
            Powered by Intent Classification &amp; Named Entity Recognition.
          </p>
        </section>

        {/* Search */}
        <div style={{ animation: "fadeUp 0.5s ease 0.2s both" }}>
          <div style={{
            display: "flex", alignItems: "center",
            background: focused ? "rgba(0,212,170,0.04)" : "rgba(255,255,255,0.04)",
            border: `1px solid ${focused ? "rgba(0,212,170,0.4)" : "rgba(255,255,255,0.08)"}`,
            borderRadius: 14, padding: "0 8px 0 18px", height: 60,
            transition: "all 0.25s ease",
            boxShadow: focused ? "0 0 0 4px rgba(0,212,170,0.07)" : "none",
          }}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
              stroke={focused ? "rgba(0,212,170,0.8)" : "rgba(255,255,255,0.22)"}
              strokeWidth="2" style={{ flexShrink: 0, marginRight: 12, transition: "stroke 0.25s" }}>
              <circle cx="11" cy="11" r="8" /><path d="M21 21l-4.35-4.35" />
            </svg>

            <div style={{ flex: 1, position: "relative", height: "100%", display: "flex", alignItems: "center" }}>
              {!query && (
                <div style={{ position: "absolute", left: 0, pointerEvents: "none", width: "100%", overflow: "hidden", whiteSpace: "nowrap" }}>
                  <TypingPlaceholder />
                </div>
              )}
              <input
                ref={inputRef}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onFocus={() => setFocused(true)}
                onBlur={() => setFocused(false)}
                onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                style={{ width: "100%", background: "transparent", border: "none", outline: "none", fontSize: 15, color: "#e8edf5", caretColor: "#00d4aa" }}
              />
            </div>

            <button className="send-btn" onClick={handleSearch} style={{ width: 40, height: 40, borderRadius: 9, flexShrink: 0, background: "rgba(0,212,170,0.1)", border: "1px solid rgba(0,212,170,0.25)", display: "flex", alignItems: "center", justifyContent: "center" }}>
              {loading
                ? <div style={{ width: 14, height: 14, border: "2px solid rgba(0,212,170,0.2)", borderTop: "2px solid #00d4aa", borderRadius: "50%", animation: "spin 0.8s linear infinite" }} />
                : <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#00d4aa" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14M12 5l7 7-7 7" /></svg>
              }
            </button>
          </div>

          {/* Company chips */}
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginTop: 12, flexWrap: "wrap" }}>
            <span style={{ fontFamily: "monospace", fontSize: 10, letterSpacing: "0.08em", color: "rgba(255,255,255,0.2)", textTransform: "uppercase", flexShrink: 0 }}>Quick select</span>
            {COMPANIES.map((c) => {
              const active = activeCompany === c.name;
              return (
                <button key={c.name} className="chip-btn" onClick={() => handleCompanyClick(c)} style={{ display: "flex", alignItems: "center", gap: 7, padding: "7px 13px", background: active ? `${c.color}14` : "rgba(255,255,255,0.04)", border: `1px solid ${active ? c.color + "55" : "rgba(255,255,255,0.08)"}`, borderRadius: 8, color: active ? c.color : "rgba(255,255,255,0.45)", fontFamily: "monospace", fontSize: 12 }}>
                  <span style={{ width: 6, height: 6, borderRadius: "50%", background: c.color, opacity: active ? 1 : 0.55, flexShrink: 0 }} />
                  {c.name}
                </button>
              );
            })}
          </div>
        </div>

        {/* Loading skeleton */}
        {loading && (
          <div style={{ marginTop: 34 }}>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 12, marginBottom: 14 }}>
              {[1,2,3,4].map(i => (
                <div key={i} style={{ background: "rgba(255,255,255,0.03)", borderRadius: 12, padding: "18px 20px", height: 85 }}>
                  {[60,80].map((w,j) => (
                    <div key={j} style={{ height: j===0?9:17, width:`${w}%`, borderRadius: 4, marginBottom: 10, background: "linear-gradient(90deg,rgba(255,255,255,0.04) 25%,rgba(255,255,255,0.09) 50%,rgba(255,255,255,0.04) 75%)", backgroundSize:"200% 100%", animation:"shimmer 1.4s infinite" }} />
                  ))}
                </div>
              ))}
            </div>
            <div style={{ background: "rgba(255,255,255,0.025)", borderRadius: 14, padding: "30px 34px" }}>
              {[100,88,94,72,85,60].map((w,i) => (
                <div key={i} style={{ height: 11, width:`${w}%`, borderRadius: 4, marginBottom: 13, background: "linear-gradient(90deg,rgba(255,255,255,0.03) 25%,rgba(255,255,255,0.07) 50%,rgba(255,255,255,0.03) 75%)", backgroundSize:"200% 100%", animation:"shimmer 1.4s infinite" }} />
              ))}
            </div>
          </div>
        )}

        {/* Insight panel */}
        {insight && !loading && (
          <div style={{ marginTop: 34, animation: "fadeUp 0.45s ease both" }}>
            {insight.metrics.length > 0 && (
              <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 12, marginBottom: 14 }}>
                {insight.metrics.map((m, i) => <MetricCard key={m.label} {...m} delay={i * 70} />)}
              </div>
            )}
            <div style={{ background: "rgba(255,255,255,0.025)", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 16, padding: "32px 36px" }}>
              <div style={{ marginBottom: 24 }}>
                <div style={{ width: 30, height: 2, background: "linear-gradient(90deg,#00d4aa,transparent)", borderRadius: 2, marginBottom: 14 }} />
                <h2 style={{ fontWeight: 700, fontSize: 20, letterSpacing: "-0.025em", color: "#e8edf5", marginBottom: 10 }}>{insight.title}</h2>
                <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
                  {["FY2024", "NER Extracted", "Intent: Summary"].map(tag => (
                    <span key={tag} style={{ fontFamily: "monospace", fontSize: 10, letterSpacing: "0.07em", color: "rgba(255,255,255,0.25)", textTransform: "uppercase" }}>{tag}</span>
                  ))}
                </div>
              </div>
              {insight.body.map((para, i) => (
                <p key={i} style={{ fontSize: 15, fontWeight: 300, lineHeight: 1.85, color: "rgba(232,237,245,0.68)", marginBottom: i < insight.body.length - 1 ? 16 : 0 }}>{para}</p>
              ))}
              <div style={{ marginTop: 26, paddingTop: 16, borderTop: "1px solid rgba(255,255,255,0.06)" }}>
                <span style={{ fontFamily: "monospace", fontSize: 10, color: "rgba(255,255,255,0.18)", letterSpacing: "0.04em" }}>
                  Generated by Documind · NER + Intent Classification · Data from publicly filed reports
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Empty state */}
        {!insight && !loading && (
          <div style={{ textAlign: "center", padding: "58px 0 30px", animation: "fadeUp 0.5s ease 0.3s both" }}>
            <div style={{ display: "flex", justifyContent: "center", marginBottom: 16 }}>
              <svg width="38" height="38" viewBox="0 0 40 40" fill="none">
                <rect x="5" y="9" width="30" height="24" rx="4" stroke="rgba(0,212,170,0.25)" strokeWidth="1.5" />
                <path d="M11 17h18M11 21h12M11 25h14" stroke="rgba(0,212,170,0.2)" strokeWidth="1.5" strokeLinecap="round" />
                <circle cx="30" cy="12" r="6" fill="rgba(0,212,170,0.08)" stroke="rgba(0,212,170,0.2)" strokeWidth="1.2" />
                <path d="M28 12h4M30 10v4" stroke="#00d4aa" strokeWidth="1.3" strokeLinecap="round" opacity="0.5" />
              </svg>
            </div>
            <p style={{ fontSize: 14, fontWeight: 300, color: "rgba(255,255,255,0.28)", marginBottom: 8 }}>Select a company above or enter a financial query to begin</p>
            <p style={{ fontFamily: "monospace", fontSize: 11, color: "rgba(0,212,170,0.3)", letterSpacing: "0.04em" }}>Try: "Compare revenue of TCS and Infosys in 2024"</p>
          </div>
        )}

      </div>
    </div>
  );
}
