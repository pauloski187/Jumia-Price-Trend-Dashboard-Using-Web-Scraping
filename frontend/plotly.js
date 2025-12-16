async function fetchChartData() {
  const statusEl = document.getElementById('status');
  try {
    statusEl.textContent = 'Loading…';
    const res = await fetch('/api/price_trend');
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`API ${res.status}: ${txt}`);
    }
    const data = await res.json();
    statusEl.textContent = '';
    return data;
  } catch (err) {
    console.error(err);
    statusEl.textContent = 'Failed to load data: ' + err.message;
    return null;
  }
}

function applyChartType(traces, mode) {
  return traces.map(t => ({ ...t, mode }));
}

async function renderChart() {
  const sel = document.getElementById('chartType');
  const preferredMode = sel ? sel.value : 'lines+markers';
  const chartEl = document.getElementById('chart');

  const payload = await fetchChartData();
  if (!payload) return;

  const traces = applyChartType(payload.traces || [], preferredMode);
  const layout = payload.layout || {};

  const config = { responsive: true, displaylogo: false, modeBarButtonsToRemove: ['lasso2d', 'select2d'] };
  Plotly.newPlot(chartEl, traces, layout, config);
}

document.getElementById('refreshBtn')?.addEventListener('click', renderChart);
document.getElementById('chartType')?.addEventListener('change', renderChart);

// initial render
renderChart();
