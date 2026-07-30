// Triqui — Tic-Tac-Toe V2 (Vanilla JS, IIFE)
// Features: PvP, AI (Easy/Impossible), localStorage leaderboard, animated win

(function () {
  'use strict';

  /* ── Constants ─────────────────────────────────────── */
  const WINNING_COMBOS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
  ];

  /* ── DOM References ────────────────────────────────── */
  const boardEl        = document.getElementById('board');
  const turnMarkEl     = document.getElementById('turnMark');
  const statusMsgEl    = document.getElementById('statusMsg');
  const scoreXEl       = document.getElementById('scoreXVal');
  const scoreOEl       = document.getElementById('scoreOVal');
  const scoreDrawsEl   = document.getElementById('scoreDrawsVal');
  const resetBtn       = document.getElementById('resetBtn');
  const resetScoreBtn  = document.getElementById('resetScoreBtn');
  const leaderboardBtn = document.getElementById('leaderboardBtn');
  const modeBtns       = document.querySelectorAll('.mode-btn');
  const diffBtns       = document.querySelectorAll('.diff-btn');
  const winLine        = document.getElementById('winLine');
  const boardWrapper   = document.getElementById('boardWrapper');
  const diffToggle     = document.getElementById('difficultyToggle');

  /* Leaderboard modal elements */
  const lbModal        = document.getElementById('leaderboardModal');
  const lbBody         = document.getElementById('leaderboardBody');
  const lbClose        = document.getElementById('leaderboardClose');
  const lbClear        = document.getElementById('leaderboardClearBtn');

  /* ── State ─────────────────────────────────────────── */
  let cells        = [];
  let board        = Array(9).fill(null);
  let current      = 'X';
  let active       = true;
  let mode         = 'pvp';       // 'pvp' | 'pvia'
  let difficulty   = 'impossible'; // 'easy' | 'impossible'
  let aiSymbol     = 'O';
  let humanSymbol  = 'X';
  let iaThinking   = false;

  /* ── Scores (bootstrapped from localStorage) ──────── */
  let scores = loadScores();

  function loadScores() {
    try {
      const raw = localStorage.getItem('triqui_scores');
      if (raw) {
        const parsed = JSON.parse(raw);
        if (parsed && typeof parsed.X === 'number' && typeof parsed.O === 'number' && typeof parsed.draws === 'number') {
          return parsed;
        }
      }
    } catch (_) { /* ignore corrupt data */ }
    return { X: 0, O: 0, draws: 0 };
  }

  function saveScores() {
    try { localStorage.setItem('triqui_scores', JSON.stringify(scores)); } catch (_) {}
  }

  function renderStats() {
    scoreXEl.textContent     = scores.X;
    scoreOEl.textContent     = scores.O;
    scoreDrawsEl.textContent = scores.draws;
  }

  /* ── Leaderboard ──────────────────────────────────── */
  const LB_KEY = 'triqui_leaderboard';
  const LB_MAX = 50;

  function loadLeaderboard() {
    try {
      const raw = localStorage.getItem(LB_KEY);
      if (raw) return JSON.parse(raw);
    } catch (_) {}
    return [];
  }

  function saveLeaderboard(lb) {
    try { localStorage.setItem(LB_KEY, JSON.stringify(lb)); } catch (_) {}
  }

  function addLeaderboardEntry(result, mode, difficulty) {
    const lb = loadLeaderboard();
    lb.unshift({
      result,       // 'X' | 'O' | 'draw'
      mode,         // 'pvp' | 'pvia'
      difficulty,   // 'easy' | 'impossible' | null
      timestamp: Date.now()
    });
    if (lb.length > LB_MAX) lb.length = LB_MAX;
    saveLeaderboard(lb);
  }

  function renderLeaderboard() {
    const lb = loadLeaderboard();
    if (lb.length === 0) {
      lbBody.innerHTML = '<p class="leaderboard-empty">No hay partidas registradas aún.</p>';
      return;
    }

    const medals = ['gold', 'silver', 'bronze'];
    const resultLabel = { X: 'Ganó X', O: 'Ganó O', draw: 'Empate' };
    const resultClass = { X: 'x-win', O: 'o-win', draw: 'draw' };
    const modeLabel = { pvp: 'PvP', pvia: 'vs IA' };
    const diffLabel = { easy: 'Fácil', impossible: 'Imposible' };

    const html = lb.slice(0, 20).map((e, i) => {
      const date = new Date(e.timestamp);
      const dateStr = date.toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: '2-digit' }) +
                      ' · ' + date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
      const medalClass = i < 3 ? medals[i] : '';
      const modeStr = e.mode === 'pvia' ? `${modeLabel[e.mode]} (${diffLabel[e.difficulty]})` : modeLabel[e.mode];
      return `
        <li class="lb-entry lb-${e.result === 'draw' ? 'draw' : 'win'}">
          <span class="lb-rank ${medalClass}">#${i + 1}</span>
          <div class="lb-info">
            <div class="lb-result ${resultClass[e.result]}">${resultLabel[e.result]}</div>
            <div class="lb-mode">${modeStr}</div>
          </div>
          <span class="lb-date">${dateStr}</span>
        </li>`;
    }).join('');

    lbBody.innerHTML = `<ul class="leaderboard-list">${html}</ul>`;
  }

  function clearLeaderboard() {
    saveLeaderboard([]);
    renderLeaderboard();
  }

  /* ── SVG gradient defs (injected once) ───────────── */
  function ensureSVGDefs() {
    if (winLine.querySelector('defs')) return;
    const svg = winLine;
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    defs.innerHTML = `
      <linearGradient id="winGradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#4ade80"/>
        <stop offset="50%" stop-color="#22d3ee"/>
        <stop offset="100%" stop-color="#a78bfa"/>
      </linearGradient>`;
    svg.insertBefore(defs, svg.firstChild);
  }

  /* ── Board ─────────────────────────────────────────── */
  function createBoard() {
    boardEl.innerHTML = '';
    cells = [];
    for (let i = 0; i < 9; i++) {
      const cell = document.createElement('div');
      cell.classList.add('cell');
      cell.dataset.index = i;
      cell.addEventListener('click', onCellClick);
      boardEl.appendChild(cell);
      cells.push(cell);
    }
  }

  function onCellClick(e) {
    if (iaThinking || !active) return;
    const idx = e.target.dataset.index;
    if (!active || board[idx]) return;
    makeMove(idx, current);

    if (mode === 'pvia' && active) {
      iaThinking = true;
      boardEl.classList.add('ia-thinking');
      const delay = difficulty === 'easy' ? 400 : 300;
      setTimeout(() => {
        aiMove();
        iaThinking = false;
        boardEl.classList.remove('ia-thinking');
      }, delay);
    }
  }

  function makeMove(idx, player) {
    board[idx] = player;
    const cell = cells[idx];
    cell.classList.add('taken');

    const span = document.createElement('span');
    span.textContent = player;
    span.classList.add('pop');
    span.classList.add(player === 'X' ? 'x' : 'o');
    cell.appendChild(span);
    playMove();

    const winner = checkWinner(board);
    if (winner) {
      endGame(winner.combo, player);
      return;
    }
    if (board.every(c => c !== null)) {
      endGame(null, null, true);
      return;
    }

    current = current === 'X' ? 'O' : 'X';
    updateTurn();
  }

  function updateTurn() {
    turnMarkEl.textContent = current;
    turnMarkEl.className = `mark ${current.toLowerCase()}`;
  }

  function endGame(winCombo, winner, isDraw = false) {
    active = false;
    cells.forEach(c => c.classList.add('game-over'));

    if (isDraw) {
      statusMsgEl.textContent = '¡Empate!';
      statusMsgEl.className = 'status-message draw';
      scores.draws++;
      addLeaderboardEntry('draw', mode, mode === 'pvia' ? difficulty : null);
      boardEl.classList.add('shake');
      setTimeout(() => boardEl.classList.remove('shake'), 600);
      playDraw();
    } else if (winner) {
      const winText = winner === humanSymbol ? '¡Ganaste!' : '¡Ganó la IA!';
      statusMsgEl.textContent = mode === 'pvp' ? `¡Ganó ${winner}!` : winText;
      statusMsgEl.className = 'status-message win';
      scores[winner]++;
      if (winCombo) highlightWin(winCombo);
      if (winCombo) drawWinLine(winCombo);
      triggerConfetti();
      addLeaderboardEntry(winner, mode, mode === 'pvia' ? difficulty : null);
      playWin();
    }

    saveScores();
    renderStats();
  }

  function highlightWin(combo) {
    combo.forEach(i => cells[i].classList.add('win'));
  }

  /* ── SVG Win Line ─────────────────────────────────── */
  function drawWinLine(combo) {
    if (!winLine || !combo || combo.length < 2) return;
    ensureSVGDefs();

    const [a, , c] = combo;
    const cellA = cells[a].getBoundingClientRect();
    const cellC = cells[c].getBoundingClientRect();
    const wrap  = boardWrapper.getBoundingClientRect();

    const x1 = cellA.left + cellA.width / 2 - wrap.left;
    const y1 = cellA.top + cellA.height / 2 - wrap.top;
    const x2 = cellC.left + cellC.width / 2 - wrap.left;
    const y2 = cellC.top + cellC.height / 2 - wrap.top;

    let line = winLine.querySelector('line');
    if (!line) {
      line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      winLine.appendChild(line);
    }

    line.setAttribute('x1', x1);
    line.setAttribute('y1', y1);
    line.setAttribute('x2', x2);
    line.setAttribute('y2', y2);

    winLine.classList.add('show');
  }

  /* ── Confetti effect ─────────────────────────────── */
  function triggerConfetti() {
    let overlay = boardWrapper.querySelector('.confetti-overlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.classList.add('confetti-overlay');
      boardWrapper.appendChild(overlay);
    }
    overlay.innerHTML = '';
    const colors = ['#4ade80','#22d3ee','#ffd200','#f472b6','#a78bfa','#fb923c'];
    for (let i = 0; i < 24; i++) {
      const dot = document.createElement('div');
      const size = 4 + Math.random() * 6;
      const angle = (i / 24) * Math.PI * 2;
      const radius = 20 + Math.random() * 40;
      dot.style.cssText = `
        position: absolute;
        width: ${size}px; height: ${size}px;
        border-radius: 50%;
        background: ${colors[i % colors.length]};
        left: 50%; top: 50%;
        transform: translate(-50%, -50%);
        animation: confetti-particle .7s ease-out forwards;
        --dx: ${Math.cos(angle) * radius}px;
        --dy: ${Math.sin(angle) * radius}px;
      `;
      overlay.appendChild(dot);
    }
    overlay.classList.add('active');
    setTimeout(() => overlay.classList.remove('active'), 900);
  }

  function checkWinner(b) {
    for (const combo of WINNING_COMBOS) {
      const [a, b1, c1] = combo;
      if (b[a] && b[a] === b[b1] && b[a] === b[c1]) {
        return { winner: b[a], combo };
      }
    }
    return null;
  }

  /* ── AI Moves ────────────────────────────────────── */
  function aiMove() {
    if (!active) return;
    let idx;
    if (difficulty === 'easy') {
      idx = randomMove();
    } else {
      idx = bestMove();
    }
    if (idx !== -1) makeMove(idx, current);
  }

  function randomMove() {
    const available = board.map((v, i) => v === null ? i : -1).filter(i => i !== -1);
    if (available.length === 0) return -1;
    return available[Math.floor(Math.random() * available.length)];
  }

  function bestMove() {
    let best = -1;
    let bestVal = -Infinity;
    for (let i = 0; i < 9; i++) {
      if (!board[i]) {
        board[i] = aiSymbol;
        const val = minimax(board, 0, false, -Infinity, Infinity);
        board[i] = null;
        if (val > bestVal) {
          bestVal = val;
          best = i;
        }
      }
    }
    return best;
  }

  function minimax(b, depth, isMax, alpha, beta) {
    const res = checkWinner(b);
    if (res) return res.winner === aiSymbol ? 10 - depth : depth - 10;
    if (b.every(c => c !== null)) return 0;

    if (isMax) {
      let maxEval = -Infinity;
      for (let i = 0; i < 9; i++) {
        if (!b[i]) {
          b[i] = aiSymbol;
          const ev = minimax(b, depth + 1, false, alpha, beta);
          b[i] = null;
          maxEval = Math.max(maxEval, ev);
          alpha = Math.max(alpha, ev);
          if (beta <= alpha) break;
        }
      }
      return maxEval;
    } else {
      let minEval = Infinity;
      for (let i = 0; i < 9; i++) {
        if (!b[i]) {
          b[i] = humanSymbol;
          const ev = minimax(b, depth + 1, true, alpha, beta);
          b[i] = null;
          minEval = Math.min(minEval, ev);
          beta = Math.min(beta, ev);
          if (beta <= alpha) break;
        }
      }
      return minEval;
    }
  }

  /* ── Reset ──────────────────────────────────────────── */
  function resetBoard() {
    board.fill(null);
    active    = true;
    current   = 'X';
    iaThinking = false;
    boardEl.classList.remove('ia-thinking', 'shake');
    updateTurn();
    statusMsgEl.textContent = '¡A jugar!';
    statusMsgEl.className = 'status-message';

    cells.forEach(c => {
      c.classList.remove('taken', 'game-over', 'win');
      c.innerHTML = '';
    });

    if (winLine) {
      winLine.classList.remove('show');
      const line = winLine.querySelector('line');
      if (line) {
        line.setAttribute('x1', 0); line.setAttribute('y1', 0);
        line.setAttribute('x2', 0); line.setAttribute('y2', 0);
      }
    }
  }

  function resetAllScores() {
    if (!confirm('¿Resetear todos los puntajes?')) return;
    scores = { X: 0, O: 0, draws: 0 };
    saveScores();
    renderStats();
  }

  /* ── Mode & Difficulty Toggle ─────────────────────── */
  function setMode(m) {
    mode = m;
    modeBtns.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.mode === m);
    });
    diffToggle.style.display = m === 'pvia' ? 'flex' : 'none';
    resetBoard();
  }

  function setDifficulty(d) {
    difficulty = d;
    diffBtns.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.diff === d);
    });
    resetBoard();
  }

  /* ── Leaderboard Modal ────────────────────────────── */
  function openLeaderboard() {
    renderLeaderboard();
    lbModal.classList.add('open');
  }

  function closeLeaderboard() {
    lbModal.classList.remove('open');
  }

  /* ── Theme Toggle ───────────────────────────────────── */
  const themeBtn = document.getElementById('themeBtn');
  let currentTheme = localStorage.getItem('triqui_theme') || 'dark';

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    themeBtn.textContent = theme === 'dark' ? '🌙' : '☀️';
    localStorage.setItem('triqui_theme', theme);
  }

  themeBtn.addEventListener('click', () => {
    currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(currentTheme);
  });

  applyTheme(currentTheme);

  /* ── Sound Effects (Web Audio API) ─────────────────── */
  let audioCtx = null;
  function ensureAudio() {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    return audioCtx;
  }
  function playTone(freq, duration, type = 'sine', volume = 0.15) {
    const ctx = ensureAudio();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = type;
    osc.frequency.value = freq;
    osc.connect(gain);
    gain.connect(ctx.destination);
    gain.gain.setValueAtTime(volume, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + duration);
  }
  function playMove() { playTone(440 + Math.random() * 100, 0.08, 'square', 0.1); }
  function playWin() {
    playTone(523, 0.12, 'sine', 0.2);
    setTimeout(() => playTone(659, 0.12, 'sine', 0.2), 120);
    setTimeout(() => playTone(784, 0.2, 'sine', 0.2), 240);
  }
  function playDraw() { playTone(300, 0.15, 'triangle', 0.12); }

  /* ── Event Listeners ──────────────────────────────── */
  resetBtn.addEventListener('click', resetBoard);
  resetScoreBtn.addEventListener('click', resetAllScores);
  leaderboardBtn.addEventListener('click', openLeaderboard);
  lbClose.addEventListener('click', closeLeaderboard);
  lbModal.addEventListener('click', e => { if (e.target === lbModal) closeLeaderboard(); });
  lbClear.addEventListener('click', () => { clearLeaderboard(); });

  modeBtns.forEach(btn => btn.addEventListener('click', () => setMode(btn.dataset.mode)));
  diffBtns.forEach(btn => btn.addEventListener('click', () => setDifficulty(btn.dataset.diff)));

  /* ── Inject confetti keyframes ────────────────────── */
  const style = document.createElement('style');
  style.textContent = `
@keyframes confetti-particle {
  0%   { opacity: 1; transform: translate(-50%, -50%) scale(1); }
  100% { opacity: 0; transform: translate(calc(-50% + var(--dx)), calc(-50% + var(--dy))) scale(0.3); }
}`;
  document.head.appendChild(style);

  /* ── Service Worker Registration ─────────────────── */
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('sw.js').catch(() => {});
    });
  }

  /* ── Init ──────────────────────────────────────────── */
  createBoard();
  renderStats();
  ensureSVGDefs();
})();