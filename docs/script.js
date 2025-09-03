/* global fetch */
(function () {
  const canvas = document.getElementById('grid');
  const ctx = canvas.getContext('2d');
  const playBtn = document.getElementById('play');
  const pauseBtn = document.getElementById('pause');
  const stepRange = document.getElementById('stepRange');
  const stepLabel = document.getElementById('stepLabel');
  const logEl = document.getElementById('log');
  const summaryEl = document.getElementById('summary');

  let data = null;
  let timer = null;

  function draw(snapshot) {
    const { resources, agents } = snapshot;
    const width = resources.width;
    const height = resources.height;
    const cells = resources.cells;

    const cellSize = Math.min(canvas.width / width, canvas.height / height);
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw resources as heatmap
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const v = cells[y][x];
        const intensity = Math.min(1, v / 10);
        ctx.fillStyle = `rgba(46, 204, 113, ${0.1 + 0.7 * intensity})`;
        ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
      }
    }

    // Draw agents
    for (const a of agents) {
      ctx.beginPath();
      ctx.fillStyle = a.strategy === 'cooperate' ? '#2e86de' : '#e74c3c';
      ctx.arc((a.x + 0.5) * cellSize, (a.y + 0.5) * cellSize, Math.max(2, cellSize * 0.35), 0, Math.PI * 2);
      ctx.fill();
    }
  }

  function updateSummary(snapshot) {
    const counts = snapshot.agents.reduce(
      (acc, a) => {
        acc.total += 1;
        if (a.energy > 0) acc.alive += 1;
        if (a.strategy === 'cooperate') acc.coop += 1; else acc.comp += 1;
        return acc;
      },
      { total: 0, alive: 0, coop: 0, comp: 0 }
    );
    summaryEl.textContent = `에이전트 ${counts.total} (생존 ${counts.alive}) | 협력 ${counts.coop} / 경쟁 ${counts.comp}`;
  }

  function setStep(i) {
    const snapshot = data.snapshots[i];
    draw(snapshot);
    updateSummary(snapshot);
    stepLabel.textContent = `Step: ${snapshot.step}`;
  }

  function start() {
    if (timer) return;
    timer = setInterval(() => {
      let v = Number(stepRange.value);
      v = (v + 1) % data.snapshots.length;
      stepRange.value = String(v);
      setStep(v);
    }, 300);
  }

  function stop() {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
  }

  playBtn.addEventListener('click', start);
  pauseBtn.addEventListener('click', stop);
  stepRange.addEventListener('input', (e) => setStep(Number(e.target.value)));

  fetch('data/sim.json', { cache: 'no-store' })
    .then((r) => r.json())
    .then((json) => {
      data = json;
      stepRange.max = String(data.snapshots.length - 1);
      stepRange.value = '0';
      setStep(0);
      // Render recent log
      logEl.textContent = (data.log || []).slice(-100).join('\n');
    })
    .catch((e) => {
      logEl.textContent = '데이터를 불러오지 못했습니다. 먼저 로컬에서 main.py를 실행해 docs/data/sim.json을 생성하세요.';
      console.error(e);
    });
})();

