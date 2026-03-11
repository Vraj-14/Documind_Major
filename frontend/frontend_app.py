# import streamlit as st
# import requests
# import pandas as pd

# # Backend API URL
# API_URL = "http://127.0.0.1:8000/ask"

# st.set_page_config(
#     page_title="Documind Financial Assistant",
#     page_icon="📊",
#     layout="wide"
# )

# st.title("📊 Documind AI Financial Assistant")

# st.write(
#     "Ask financial questions about NIFTY 50 companies."
# )

# # -----------------------------
# # User Question Input
# # -----------------------------

# question = st.text_input(
#     "Enter your financial question",
#     placeholder="Example: Compare HDFC Bank Limited and ICICI Bank Limited net profit for 2023"
# )

# # -----------------------------
# # Submit Button
# # -----------------------------

# if st.button("Ask Question"):

#     if question.strip() == "":
#         st.warning("Please enter a question.")
#     else:

#         with st.spinner("Analyzing financial data..."):

#             response = requests.post(
#                 API_URL,
#                 json={"question": question}
#             )

#             result = response.json()

#         # -----------------------------
#         # Display AI Answer
#         # -----------------------------

#         st.subheader("💡 AI Answer")

#         st.success(result["answer"])

#         # -----------------------------
#         # Display Extracted Entities
#         # -----------------------------

#         st.subheader("🔍 Extracted Entities")

#         st.json(result["entities"])

#         # -----------------------------
#         # Display SQL Query
#         # -----------------------------

#         st.subheader("🧠 Generated SQL Query")

#         st.code(result["sql_query"], language="sql")

#         # -----------------------------
#         # Display Financial Data
#         # -----------------------------

#         st.subheader("📑 Financial Data")

#         if result["data"]:

#             df = pd.DataFrame(
#                 result["data"],
#                 columns=result["entities"].get("COMPANY", [])[:len(result["data"][0])]
#                 if "COMPANY" in result["entities"] else None
#             )

#             st.dataframe(df)

#         else:
#             st.info("No data returned from database.")




import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="Documind · Financial Intelligence",
    page_icon="📈",
    layout="wide"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0c10 !important;
    color: #e8eaf0;
    font-family: 'DM Mono', monospace;
}

[data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
[data-testid="stAppViewContainer"] > .main > div { padding-top: 0 !important; }
section[data-testid="stMain"] > div { padding-top: 0 !important; }
[data-testid="stSidebar"] { display: none; }
header[data-testid="stHeader"] { display: none; }
[data-testid="stToolbar"] { display: none; }
footer { display: none; }

/* ── Layout wrapper ── */
.dm-shell {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    max-width: 860px;
    margin: 0 auto;
    padding: 12px 24px 120px;
}

/* ── Wordmark ── */
.dm-wordmark {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 28px;
    letter-spacing: -0.5px;
    color: #fff;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.dm-wordmark span.dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #ff7a00;
    margin-bottom: 2px;
}
.dm-sub {
    font-size: 11px;
    color: #7a6a5a;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 32px;
}

/* ── Section labels ── */
.dm-label {
    font-size: 10px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #7a6a5a;
    margin-bottom: 12px;
    font-family: 'DM Mono', monospace;
}

/* ── Company pills ── */
.dm-company-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 32px;
}
.dm-pill {
    padding: 8px 16px;
    border-radius: 100px;
    border: 1px solid #2a1f14;
    background: #151008;
    color: #8a7a6a;
    font-size: 12px;
    font-family: 'DM Mono', monospace;
    cursor: pointer;
    transition: all 0.18s ease;
    user-select: none;
    white-space: nowrap;
}
.dm-pill:hover {
    border-color: #ff7a00;
    color: #ff7a00;
    background: #1a0f00;
}
.dm-pill.active {
    border-color: #ff7a00;
    background: #1a0f00;
    color: #ff7a00;
    font-weight: 500;
}

/* ── Performance toggle ── */
.dm-perf-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 36px;
}
.dm-toggle-label {
    font-size: 11px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #4a5060;
}
.dm-toggle-wrap {
    position: relative;
    width: 40px;
    height: 22px;
}
.dm-toggle-wrap input { opacity: 0; width: 0; height: 0; }
.dm-toggle-slider {
    position: absolute;
    cursor: pointer;
    inset: 0;
    background: #1e2230;
    border-radius: 22px;
    transition: background 0.2s;
}
.dm-toggle-slider:before {
    content: '';
    position: absolute;
    width: 16px; height: 16px;
    left: 3px; top: 3px;
    background: #4a5060;
    border-radius: 50%;
    transition: transform 0.2s, background 0.2s;
}
input:checked + .dm-toggle-slider { background: #1a0f00; border: 1px solid #ff7a00; }
input:checked + .dm-toggle-slider:before { transform: translateX(18px); background: #ff7a00; }
.dm-perf-active { color: #ff7a00 !important; }

/* ── Input box ── */
.dm-input-wrap {
    position: relative;
    margin-bottom: 32px;
}
.dm-input-outer {
    display: flex;
    align-items: flex-end;
    gap: 0;
    background: #f5f0eb;
    border: 1px solid #d4c8bc;
    border-radius: 14px;
    padding: 14px 14px 14px 18px;
    transition: border-color 0.2s;
}
.dm-input-outer:focus-within { border-color: #ff7a00; }

/* hide streamlit textarea's own border */
.dm-input-outer textarea {
    flex: 1;
    background: transparent !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    color: #1a1008 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 14px !important;
    resize: none !important;
    min-height: 24px !important;
    line-height: 1.6 !important;
    caret-color: #ff7a00;
}

/* ── Send button ── */
.dm-send-btn {
    width: 36px; height: 36px;
    border-radius: 9px;
    background: #ff7a00;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: background 0.18s, transform 0.12s;
}
.dm-send-btn:hover { background: #e56d00; transform: translateY(-1px); }
.dm-send-btn:active { transform: translateY(0); }
.dm-send-btn svg { width: 16px; height: 16px; fill: #fff; }

/* ── Divider ── */
.dm-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #2a1f14 30%, #2a1f14 70%, transparent);
    margin: 12px 0 32px;
}

/* ── Answer card ── */
.dm-answer-card {
    background: #130e08;
    border: 1px solid #2a1f14;
    border-radius: 14px;
    padding: 28px 28px 24px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.dm-answer-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #ff7a00, #c25500);
    border-radius: 14px 0 0 14px;
}
.dm-answer-label {
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #ff7a00;
    margin-bottom: 14px;
    font-family: 'DM Mono', monospace;
}
.dm-answer-text {
    font-size: 14px;
    line-height: 1.8;
    color: #d4c8b8;
    white-space: pre-wrap;
}

/* ── Metadata cards ── */
.dm-meta-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-bottom: 24px;
}
@media (max-width: 600px) { .dm-meta-row { grid-template-columns: 1fr; } }

.dm-meta-card {
    background: #0e0a05;
    border: 1px solid #221810;
    border-radius: 12px;
    padding: 18px 20px;
}
.dm-meta-card-label {
    font-size: 9px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #7a6a5a;
    margin-bottom: 12px;
}
.dm-sql-text {
    font-size: 12px;
    color: #ff9a40;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-all;
}
.dm-entity-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}
.dm-entity-chip {
    font-size: 11px;
    padding: 3px 10px;
    border-radius: 100px;
    background: #1a1208;
    border: 1px solid #2e2010;
    color: #8a7a6a;
}
.dm-entity-chip b {
    color: #ff7a00;
    font-weight: 500;
    margin-right: 4px;
}

/* ── Data table ── */
.dm-table-card {
    background: #0e0a05;
    border: 1px solid #221810;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 24px;
}
.dm-table-card-label {
    font-size: 9px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #7a6a5a;
    margin-bottom: 14px;
}

/* ── Streamlit widget overrides ── */
[data-testid="stTextArea"] textarea {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #1a1008 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 14px !important;
    padding: 0 !important;
}
[data-testid="stTextArea"] > div > div {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
div[data-baseweb="base-input"] { background: transparent !important; }

.stButton button {
    background: #ff7a00 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 9px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    padding: 8px 18px !important;
    letter-spacing: 0.5px;
    transition: background 0.18s !important;
    height: 36px !important;
}
.stButton button:hover { background: #e56d00 !important; }

/* dataframe */
[data-testid="stDataFrame"] {
    border: none !important;
}
.stDataFrame > div { border-radius: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────
if "selected_companies" not in st.session_state:
    st.session_state.selected_companies = []
if "perf_analysis" not in st.session_state:
    st.session_state.perf_analysis = False
if "result" not in st.session_state:
    st.session_state.result = None
if "last_question" not in st.session_state:
    st.session_state.last_question = ""

COMPANIES = [
    "Reliance Industries",
    "HDFC Bank Limited",
    "ICICI Bank Limited",
    "State Bank of India",
    "TCS",
]

# ── Shell open ────────────────────────────────────────────────────────────
st.markdown('<div class="dm-shell">', unsafe_allow_html=True)

# Wordmark
st.markdown("""
<div class="dm-wordmark">
    <span class="dot"></span> Documind
</div>
<div class="dm-sub">Finance Insights, Powered by AI.</div>
""", unsafe_allow_html=True)

# ── Company selector ───────────────────────────────────────────────────────
st.markdown('<div class="dm-label">Select Companies</div>', unsafe_allow_html=True)

cols = st.columns(len(COMPANIES))
for i, company in enumerate(COMPANIES):
    with cols[i]:
        is_active = company in st.session_state.selected_companies
        label = f"{'✓ ' if is_active else ''}{company.split()[0]}"  # short name
        if st.button(label, key=f"co_{i}"):
            if company in st.session_state.selected_companies:
                st.session_state.selected_companies.remove(company)
            else:
                st.session_state.selected_companies.append(company)
            st.rerun()

# Show selected
if st.session_state.selected_companies:
    chips = "".join(
        f'<span class="dm-entity-chip"><b>●</b>{c}</span>'
        for c in st.session_state.selected_companies
    )
    st.markdown(f'<div class="dm-entity-row" style="margin-top:10px;margin-bottom:4px;">{chips}</div>', unsafe_allow_html=True)

st.markdown('<div style="height:28px"></div>', unsafe_allow_html=True)

# ── Performance Analysis toggle ───────────────────────────────────────────
perf_col1, perf_col2 = st.columns([6, 1])
with perf_col1:
    st.markdown('<div class="dm-label">Analysis Mode</div>', unsafe_allow_html=True)
    perf = st.toggle("Performance Analysis", value=st.session_state.perf_analysis, key="perf_toggle")
    st.session_state.perf_analysis = perf
    if perf:
        st.markdown('<div style="font-size:11px;color:#ff7a00;letter-spacing:1px;margin-top:-8px;margin-bottom:8px;">● Performance analysis mode active — results will include performance breakdown</div>', unsafe_allow_html=True)

st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

# ── Question input ─────────────────────────────────────────────────────────
st.markdown('<div class="dm-label">Ask a Financial Question</div>', unsafe_allow_html=True)

# Build placeholder hint
if st.session_state.selected_companies:
    hint_cos = " and ".join(st.session_state.selected_companies[:2])
    placeholder = f"e.g. Compare {hint_cos} revenue for 2024"
else:
    placeholder = "e.g. What is HDFC Bank net profit for 2023?"

input_col, btn_col = st.columns([11, 1])
with input_col:
    question = st.text_area(
        label="",
        placeholder=placeholder,
        key="question_input",
        label_visibility="collapsed",
        height=56,
    )
with btn_col:
    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
    submit = st.button("↑", key="send_btn", help="Submit question")

# ── Submit logic ───────────────────────────────────────────────────────────
def build_enriched_question(q, companies, perf_mode):
    """Prepend selected companies and performance mode hint to the query."""
    enriched = q.strip()
    if companies and not any(c.lower() in enriched.lower() for c in companies):
        company_str = " and ".join(companies)
        enriched = f"{enriched} for {company_str}"
    if perf_mode and "performance" not in enriched.lower():
        enriched = "Performance analysis: " + enriched
    return enriched

if submit:
    raw_q = question.strip()
    if not raw_q:
        st.warning("Please enter a question before submitting.")
    else:
        final_q = build_enriched_question(
            raw_q,
            st.session_state.selected_companies,
            st.session_state.perf_analysis,
        )
        st.session_state.last_question = final_q

        with st.spinner(""):
            st.markdown(
                '<div style="font-size:11px;color:#4a5060;letter-spacing:1px;margin-bottom:8px;">Querying financial database…</div>',
                unsafe_allow_html=True,
            )
            try:
                resp = requests.post(API_URL, json={"question": final_q}, timeout=30)
                st.session_state.result = resp.json()
            except Exception as e:
                st.session_state.result = {"error": str(e)}
        st.rerun()

# ── Results ────────────────────────────────────────────────────────────────
if st.session_state.result:
    result = st.session_state.result
    st.markdown('<div class="dm-divider"></div>', unsafe_allow_html=True)

    if "error" in result:
        st.markdown(f"""
        <div class="dm-answer-card" style="border-color:#e85050;">
            <div class="dm-answer-label" style="color:#e85050;">Error</div>
            <div class="dm-answer-text" style="color:#c87070;">{result["error"]}</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # AI Answer
        answer_text = result.get("answer", "No answer returned.")
        st.markdown(f"""
        <div class="dm-answer-card">
            <div class="dm-answer-label">AI Answer</div>
            <div class="dm-answer-text">{answer_text}</div>
        </div>
        """, unsafe_allow_html=True)

        # Entities + SQL side by side
        entities = result.get("entities", {})
        sql = result.get("sql_query", "")

        entity_chips = ""
        for etype, values in entities.items():
            vals = values if isinstance(values, list) else [values]
            for v in vals:
                entity_chips += f'<span class="dm-entity-chip"><b>{etype}</b>{v}</span>'

        st.markdown(f"""
        <div class="dm-meta-row">
            <div class="dm-meta-card">
                <div class="dm-meta-card-label">Extracted Entities</div>
                <div class="dm-entity-row">{entity_chips if entity_chips else '<span style="color:#4a5060;font-size:12px;">None detected</span>'}</div>
            </div>
            <div class="dm-meta-card">
                <div class="dm-meta-card-label">Generated SQL</div>
                <div class="dm-sql-text">{sql if sql else "—"}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Data table
        data = result.get("data")
        if data:
            st.markdown('<div class="dm-table-card"><div class="dm-table-card-label">Financial Data</div>', unsafe_allow_html=True)
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="dm-table-card">
                <div class="dm-table-card-label">Financial Data</div>
                <span style="font-size:12px;color:#4a5060;">No records returned for this query.</span>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close .dm-shell