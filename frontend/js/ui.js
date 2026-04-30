// // Track both chart instances so we can destroy before redrawing
// let barChartInstance = null;
// let pieChartInstance = null;

// function displayAnswer(result) {

//     // ── Text answer ──────────────────────────────────────────
//     document.getElementById("answerWindow").innerText = result.answer;

//     // ── Entity tags ──────────────────────────────────────────
//     document.getElementById("company").innerText =
//         (result.entities.COMPANY || []).join(", ");

//     document.getElementById("metric").innerText =
//         (result.entities.METRIC || []).join(", ");

//     document.getElementById("year").innerText =
//         (result.entities.YEAR || []).join(", ");


//     // ── Intent debug panel ───────────────────────────────────
//     const predicted  = result.predicted_intent || result.intent;
//     const final      = result.final_intent     || result.intent;
//     const confidence = result.confidence !== null ? result.confidence : "—";
//     const overridden = result.override_fired;

//     document.getElementById("predictedIntent").innerText = predicted;
//     document.getElementById("finalIntent").innerText     = final;
//     document.getElementById("confidenceScore").innerText = confidence !== "—"
//     ? `${confidence}%`
//     : "—";

//     // Highlight the final intent card if it was overridden
//     const finalCard = document.getElementById("finalIntentCard");
//     finalCard.style.borderColor = overridden ? "#E05A2B" : "var(--border)";


//     // ── Charts ───────────────────────────────────────────────
//     renderCharts(result);
// }


// function renderCharts(result) {

//     const chartSection = document.getElementById("chartSection");

//     // Destroy previous instances
//     if (barChartInstance) { barChartInstance.destroy(); barChartInstance = null; }
//     if (pieChartInstance) { pieChartInstance.destroy(); pieChartInstance = null; }

//     const data      = result.data;
//     const intent    = result.intent;
//     const metrics   = result.entities.METRIC  || [];
//     const companies = result.entities.COMPANY || [];

//     // Hide if no data or only a single value
//     if (!data || data.length === 0) {
//         chartSection.style.display = "none";
//         return;
//     }
//     const totalValues = data.reduce((sum, row) => sum + row.length, 0);
//     if (totalValues <= 1) {
//         chartSection.style.display = "none";
//         return;
//     }

//     // ── BAR colour palette — blue monochrome (light to dark) ─
//     const BAR_COLORS = [
//         "#2563EB",
//         "#3B82F6",
//         "#60A5FA",
//         "#93C5FD",
//         "#BFDBFE",
//     ];

//     // ── PIE colour palette — multicolour with contrast ───────
//     const PIE_COLORS = [
//         "#2563EB",   // blue    (primary)
        
//         "#10B981",   // green
//         "#c43737",   // red
//         "#F59E0B",   // orange
//         "#22D3EE",   // cyan

//     ];

//     // ── Build labels & values depending on intent ────────────
//     let labels = [];
//     let values = [];

//     if (intent === "trend_analysis") {
//         labels = data.map(row => String(row[0]));
//         values = data.map(row => Number(row[1]));

//     } else if (intent === "comparison") {
//         labels = data.map(row => String(row[0]));
//         values = data.map(row => Number(row[1]));

//     } else {
//         // metric_lookup / performance_analysis
//         labels = metrics.length > 0
//             ? metrics
//             : data[0].map((_, i) => `Metric ${i + 1}`);
//         values = data[0].map(v => Number(v));
//     }

//     // ── Shared tick formatter ────────────────────────────────
//     function formatTick(value) {
//         if (Math.abs(value) >= 1e9)  return (value / 1e9).toFixed(1)  + "B";
//         if (Math.abs(value) >= 1e7)  return (value / 1e7).toFixed(1)  + "Cr";
//         if (Math.abs(value) >= 1e5)  return (value / 1e5).toFixed(1)  + "L";
//         return value;
//     }

//     const fontBase = { family: "'DM Sans', sans-serif" };

//     // ════════════════════════════════════════════════════════
//     // BAR / LINE CHART
//     // ════════════════════════════════════════════════════════
//     const barCanvas = document.getElementById("barChart");
//     const isLine    = (intent === "trend_analysis");

//     // For line: single primary blue; for bar: one shade per bar
//     const barBgColors     = isLine ? "#2563EB" : labels.map((_, i) => BAR_COLORS[i % BAR_COLORS.length]);
//     const barBorderColors = isLine ? "#1D4ED8" : labels.map((_, i) => BAR_COLORS[i % BAR_COLORS.length]);

//     barChartInstance = new Chart(barCanvas, {
//         type: isLine ? "line" : "bar",
//         data: {
//             labels,
//             datasets: [{
//                 label: metrics[0] || companies[0] || "Value",
//                 data: values,
//                 backgroundColor: barBgColors,
//                 borderColor:     barBorderColors,
//                 borderWidth: isLine ? 2.5 : 0,
//                 borderRadius: isLine ? 0 : 6,
//                 tension: 0.35,
//                 fill: false,
//                 pointRadius:      isLine ? 5 : 0,
//                 pointHoverRadius: isLine ? 7 : 0,
//                 pointBackgroundColor: "#2563EB",
//             }]
//         },
//         options: {
//             responsive: true,
//             maintainAspectRatio: false,
//             plugins: {
//                 legend: { display: false },
//                 tooltip: {
//                     backgroundColor: "#1B3A6B",
//                     titleFont: { ...fontBase, size: 12 },
//                     bodyFont:  { ...fontBase, size: 12 },
//                     padding: 10,
//                     cornerRadius: 8,
//                     callbacks: {
//                         label: ctx => " " + Number(ctx.parsed.y ?? ctx.parsed).toLocaleString("en-IN")
//                     }
//                 }
//             },
//             layout: {
//                 padding: { top: 28 }
//             },
//             scales: {
//                 x: {
//                     grid:  { color: "rgba(0,0,0,0.04)" },
//                     ticks: { font: { ...fontBase, size: 11 }, color: "#5A6A85" }
//                 },
//                 y: {
//                     grid:  { color: "rgba(0,0,0,0.05)" },
//                     ticks: {
//                         font: { ...fontBase, size: 11 },
//                         color: "#5A6A85",
//                         callback: formatTick
//                     }
//                 }
//             },
//             // ── Value labels drawn above each bar ────────────
//             animation: {
//                 onComplete: function() {
//                     if (isLine) return;
//                     const chart = this;
//                     const ctx   = chart.ctx;
//                     const ds    = chart.data.datasets[0];
//                     const meta  = chart.getDatasetMeta(0);

//                     ctx.save();
//                     ctx.font         = `600 11px 'DM Sans', sans-serif`;
//                     ctx.fillStyle    = "#1B3A6B";
//                     ctx.textAlign    = "center";
//                     ctx.textBaseline = "bottom";

//                     meta.data.forEach((bar, i) => {
//                         const label = formatTick(ds.data[i]);
//                         ctx.fillText(label, bar.x, bar.y - 5);
//                     });

//                     ctx.restore();
//                 }
//             }
//         }
//     });

//     // ════════════════════════════════════════════════════════
//     // PIE CHART
//     // ════════════════════════════════════════════════════════
//     const pieCanvas = document.getElementById("pieChart");

//     pieChartInstance = new Chart(pieCanvas, {
//         type: "pie",
//         data: {
//             labels,
//             datasets: [{
//                 data: values,
//                 backgroundColor: labels.map((_, i) => PIE_COLORS[i % PIE_COLORS.length]),
//                 borderColor:     "#FFFFFF",
//                 borderWidth: 2,
//                 hoverOffset: 10,
//             }]
//         },
//         options: {
//             responsive: true,
//             maintainAspectRatio: false,
//             plugins: {
//                 legend: {
//                     position: "bottom",
//                     labels: {
//                         font:      { ...fontBase, size: 11 },
//                         color:     "#5A6A85",
//                         padding:   12,
//                         boxWidth:  12,
//                         boxHeight: 12,
//                     }
//                 },
//                 tooltip: {
//                     backgroundColor: "#1B3A6B",
//                     titleFont: { ...fontBase, size: 12 },
//                     bodyFont:  { ...fontBase, size: 12 },
//                     padding: 10,
//                     cornerRadius: 8,
//                     callbacks: {
//                         label: ctx => {
//                             const val   = ctx.parsed;
//                             const total = ctx.dataset.data.reduce((a, b) => a + b, 0);
//                             const pct   = ((val / total) * 100).toFixed(1);
//                             return ` ${formatTick(val)}  (${pct}%)`;
//                         }
//                     }
//                 }
//             }
//         }
//     });

//     chartSection.style.display = "block";
// }


// function addHistory(question) {
//     const history = document.getElementById("history");
//     const li      = document.createElement("li");
//     li.innerText  = question;
//     history.appendChild(li);
// }





// Track both chart instances so we can destroy before redrawing
let barChartInstance = null;
let pieChartInstance = null;

function displayAnswer(result) {

    document.getElementById("answerWindow").innerText = result.answer;

    document.getElementById("company").innerText =
        (result.entities.COMPANY || []).join(", ");
    document.getElementById("metric").innerText =
        (result.entities.METRIC || []).join(", ");
    document.getElementById("year").innerText =
        (result.entities.YEAR || []).join(", ");

    const predicted  = result.predicted_intent || result.intent;
    const final      = result.final_intent     || result.intent;
    const confidence = result.confidence !== null ? result.confidence : "—";
    const overridden = result.override_fired;

    document.getElementById("predictedIntent").innerText = predicted;
    document.getElementById("finalIntent").innerText     = final;
    document.getElementById("confidenceScore").innerText = confidence !== "—"
        ? `${confidence}%` : "—";

    const finalCard = document.getElementById("finalIntentCard");
    finalCard.style.borderColor = overridden ? "#E05A2B" : "var(--border)";

    renderCharts(result);
}


function renderCharts(result) {

    const chartSection = document.getElementById("chartSection");

    if (barChartInstance) { barChartInstance.destroy(); barChartInstance = null; }
    if (pieChartInstance) { pieChartInstance.destroy(); pieChartInstance = null; }

    const data      = result.data;
    const intent    = result.intent;
    const metrics   = result.entities.METRIC  || [];
    const companies = result.entities.COMPANY || [];

    // ── DEBUG: log exactly what we received ─────────────────
    console.log("=== renderCharts ===");
    console.log("intent :", intent);
    console.log("data   :", JSON.stringify(data));
    console.log("metrics:", metrics);
    console.log("companies:", companies);

    if (!data || data.length === 0) {
        console.log("No data — hiding chart section");
        chartSection.style.display = "none";
        return;
    }

    // ── COLOUR PALETTES ──────────────────────────────────────
    const BAR_COLORS = ["#2563EB", "#3B82F6", "#60A5FA", "#93C5FD", "#BFDBFE"];
    const PIE_COLORS = ["#2563EB", "#10B981", "#c43737", "#F59E0B", "#22D3EE"];

    // ── BUILD LABELS & VALUES based on intent ────────────────
    let labels          = [];
    let values          = [];
    let isMultiDataset  = false;
    let multiDatasets   = [];   // used for grouped bar (multi-year comparison)

    if (intent === "trend_analysis") {
        // DB shape: (fiscal_year, metric_value)
        // row[0] = year, row[1] = value
        labels = data.map(row => String(row[0]));
        values = data.map(row => Number(row[1]));
        console.log("trend_analysis → labels:", labels, "values:", values);

    } else if (intent === "comparison") {
        // DB shape: (fiscal_year, company_name, metric_value)
        // row[0] = year (int), row[1] = company name (str), row[2] = value (number)
        const uniqueYears = [...new Set(data.map(row => row[0]))];
        const uniqueComps = [...new Set(data.map(row => String(row[1])))];

        console.log("comparison → uniqueYears:", uniqueYears, "uniqueComps:", uniqueComps);

        if (uniqueYears.length === 1) {
            // ── Single year: one bar per company ────────────
            labels = data.map(row => String(row[1]));          // company name
            values = data.map(row => Number(row[2]));          // metric value
            console.log("single-year comparison → labels:", labels, "values:", values);

        } else {
            // ── Multi-year: grouped bar, one dataset per company ──
            isMultiDataset = true;
            labels = uniqueYears.map(String);                  // x-axis = years

            multiDatasets = uniqueComps.map((comp, ci) => {
                const compRows = data.filter(row => String(row[1]) === comp);
                const yearMap  = {};
                compRows.forEach(r => { yearMap[r[0]] = Number(r[2]); });
                const dsValues = uniqueYears.map(y => (yearMap[y] !== undefined ? yearMap[y] : null));
                console.log(`  dataset[${ci}] company="${comp}" values:`, dsValues);
                return {
                    label:           comp,
                    data:            dsValues,
                    backgroundColor: BAR_COLORS[ci % BAR_COLORS.length],
                    borderColor:     BAR_COLORS[ci % BAR_COLORS.length],
                    borderWidth:     0,
                    borderRadius:    6,
                };
            });

            // Pie: flatten — label = "ShortName (Year)", value = metric
            labels = data.map(row => `${String(row[1]).split(" ")[0]} (${row[0]})`);
            values = data.map(row => Number(row[2]));
        }

    } else if (intent === "performance_analysis") {
        // DB shape: (fiscal_year, revenue, net_profit, eps)
        // row[0] = year — SKIP; row[1], row[2], row[3] = metric values
        const metricLabels = metrics.length > 0
            ? metrics
            : ["Revenue", "Net Profit", "EPS"];

        labels = metricLabels;
        values = data[0].slice(1).map(v => Number(v));   // slice(1) drops fiscal_year
        console.log("performance_analysis → labels:", labels, "values:", values);

    } else {
        // metric_lookup
        // Single year, single row:   (metric_val, ...)
        // Multi-year, multi rows:    (fiscal_year, metric_val)
        if (data.length > 1) {
            // Multi-year: (fiscal_year, metric)
            labels = data.map(row => String(row[0]));
            values = data.map(row => Number(row[1]));
        } else {
            // Single row: just metric values (no fiscal_year prefix)
            labels = metrics.length > 0
                ? metrics
                : data[0].map((_, i) => `Metric ${i + 1}`);
            values = data[0].map(v => Number(v));
        }
        console.log("metric_lookup → labels:", labels, "values:", values);
    }

    // ── Sanity check: hide chart if values are all NaN ───────
    const validValues = isMultiDataset
        ? multiDatasets.some(ds => ds.data.some(v => v !== null && !isNaN(v)))
        : values.some(v => !isNaN(v));

    if (!validValues) {
        console.warn("All values are NaN — hiding chart section");
        chartSection.style.display = "none";
        return;
    }

    // ── SHARED TICK FORMATTER ────────────────────────────────
    function formatTick(value) {
        if (value == null || isNaN(value)) return "";
        if (Math.abs(value) >= 1e9)  return (value / 1e9).toFixed(1)  + "B";
        if (Math.abs(value) >= 1e7)  return (value / 1e7).toFixed(1)  + "Cr";
        if (Math.abs(value) >= 1e5)  return (value / 1e5).toFixed(1)  + "L";
        return value;
    }

    const fontBase = { family: "'DM Sans', sans-serif" };

    // ════════════════════════════════════════════════════════
    // BAR / LINE CHART
    // ════════════════════════════════════════════════════════
    const barCanvas = document.getElementById("barChart");
    const isLine    = (intent === "trend_analysis");

    let finalDatasets;

    if (isMultiDataset) {
        finalDatasets = multiDatasets;
    } else {
        const barBg     = isLine ? "#2563EB"
            : labels.map((_, i) => BAR_COLORS[i % BAR_COLORS.length]);
        const barBorder = isLine ? "#1D4ED8"
            : labels.map((_, i) => BAR_COLORS[i % BAR_COLORS.length]);

        finalDatasets = [{
            label:                metrics[0] || companies[0] || "Value",
            data:                 values,
            backgroundColor:      barBg,
            borderColor:          barBorder,
            borderWidth:          isLine ? 2.5 : 0,
            borderRadius:         isLine ? 0 : 6,
            tension:              0.35,
            fill:                 false,
            pointRadius:          isLine ? 5 : 0,
            pointHoverRadius:     isLine ? 7 : 0,
            pointBackgroundColor: "#2563EB",
        }];
    }

    barChartInstance = new Chart(barCanvas, {
        type: isLine ? "line" : "bar",
        data: { labels, datasets: finalDatasets },
        options: {
            responsive:          true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: isMultiDataset },
                tooltip: {
                    backgroundColor: "#1B3A6B",
                    titleFont:       { ...fontBase, size: 12 },
                    bodyFont:        { ...fontBase, size: 12 },
                    padding:         10,
                    cornerRadius:    8,
                    callbacks: {
                        label: ctx => " " + Number(ctx.parsed.y ?? ctx.parsed).toLocaleString("en-IN")
                    }
                }
            },
            layout: { padding: { top: 28 } },
            scales: {
                x: {
                    grid:  { color: "rgba(0,0,0,0.04)" },
                    ticks: { font: { ...fontBase, size: 11 }, color: "#5A6A85" }
                },
                y: {
                    grid:  { color: "rgba(0,0,0,0.05)" },
                    ticks: {
                        font:     { ...fontBase, size: 11 },
                        color:    "#5A6A85",
                        callback: formatTick
                    }
                }
            },
            animation: {
                onComplete: function () {
                    if (isLine) return;
                    const chart = this;
                    const ctx   = chart.ctx;
                    chart.data.datasets.forEach((ds, di) => {
                        const meta = chart.getDatasetMeta(di);
                        ctx.save();
                        ctx.font         = `600 11px 'DM Sans', sans-serif`;
                        ctx.fillStyle    = "#1B3A6B";
                        ctx.textAlign    = "center";
                        ctx.textBaseline = "bottom";
                        meta.data.forEach((bar, i) => {
                            if (ds.data[i] == null || isNaN(ds.data[i])) return;
                            ctx.fillText(formatTick(ds.data[i]), bar.x, bar.y - 5);
                        });
                        ctx.restore();
                    });
                }
            }
        }
    });

    // ════════════════════════════════════════════════════════
    // PIE CHART  (always uses flat labels + values)
    // ════════════════════════════════════════════════════════
    const pieCanvas = document.getElementById("pieChart");

    // Filter out any NaN / null entries before giving to Chart.js
    const pieLabels = [];
    const pieValues = [];
    labels.forEach((lbl, i) => {
        const v = values[i];
        if (v != null && !isNaN(v)) {
            pieLabels.push(lbl);
            pieValues.push(v);
        }
    });

    console.log("pie → labels:", pieLabels, "values:", pieValues);

    pieChartInstance = new Chart(pieCanvas, {
        type: "pie",
        data: {
            labels: pieLabels,
            datasets: [{
                data:            pieValues,
                backgroundColor: pieLabels.map((_, i) => PIE_COLORS[i % PIE_COLORS.length]),
                borderColor:     "#FFFFFF",
                borderWidth:     2,
                hoverOffset:     10,
            }]
        },
        options: {
            responsive:          true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        font:      { ...fontBase, size: 11 },
                        color:     "#5A6A85",
                        padding:   12,
                        boxWidth:  12,
                        boxHeight: 12,
                    }
                },
                tooltip: {
                    backgroundColor: "#1B3A6B",
                    titleFont:       { ...fontBase, size: 12 },
                    bodyFont:        { ...fontBase, size: 12 },
                    padding:         10,
                    cornerRadius:    8,
                    callbacks: {
                        label: ctx => {
                            const val   = ctx.parsed;
                            const total = ctx.dataset.data.reduce((a, b) => a + b, 0);
                            const pct   = ((val / total) * 100).toFixed(1);
                            return ` ${formatTick(val)}  (${pct}%)`;
                        }
                    }
                }
            }
        }
    });

    chartSection.style.display = "block";
}


function addHistory(question) {
    const history = document.getElementById("history");
    const li      = document.createElement("li");
    li.innerText  = question;
    history.appendChild(li);
}