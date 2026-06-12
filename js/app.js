// Triqui — Tic-Tac-Toe (Vanilla JS, IIFE)
// Features: PvP, Player vs AI (Minimax), localStorage, SVG win-line animation

(function () {
  'use strict';

  /* ── Constants ─────────────────────────────────────── */
  const WINNING_COMBOS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
  ];

  /* ── DOM References ────────────────────────────────── */
  const boardEl      = document.getElementById('board');
  const turnMarkEl   = document.getElementById('turnMark');
  const statusMsgEl  = document.getElementById('statusMsg');
  const scoreXEl     = document.getElementById('scoreXVal');
  const scoreOEl     = document.getElementById('scoreOVal');
  const scoreDrawsEl = document.getElementById('scoreDrawsVal');
  const resetBtn     = document.getElementById('resetBtn');
  const resetScoreBtn= document.getElementById('resetScoreBtn');
  const modeBtns     = document.querySelectorAll('.mode-btn');
  const winLine      = document.getElementById('winLine');
  const boardWrapper = document.getElementById('boardWrapper');

  /* ── State ─────────────────────────────────────────── */
  let cells   = [];
  let board   = Array(9).fill(null);
  let current = 'X';
  let active  = true;
  let mode    = 'pvp';          // 'pvp' | 'pvia'
  let aiSymbol = 'O';
  let humanSymbol = 'X';

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
    const idx = e.target.dataset.index;
    if (!active || board[idx]) return;
    makeMove(idx, current);

    if (mode === 'pvia' && active) {
      setTimeout(aiMove, 300);
    }
  }

  function makeMove(idx, player) {
    board[idx] = player;
    const cell = cells[idx];
    cell.classList.add('taken');

    const span = document.createElement('span');
    span.textContent = player;
    span.classList.add('pop');
    cell.appendChild(span);

    if (cell.querySelector('span')) {
      const s = cell.querySelector('span');
      s.classList.add(player === 'X' ? 'x' : 'o');
    }

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
    } else if (winner) {
      statusMsgEl.textContent = `¡Ganó ${winner}!`;
      statusMsgEl.className = 'status-message win';
      scores[winner]++;
      highlightWin(winCombo);
      drawWinLine(winCombo);
    }

    saveScores();
    renderStats();
  }

  function highlightWin(combo) {
    combo.forEach(i => {
      cells[i].classList.add('win');
    });
  }

  /* ── SVG Win Line ──────────────────────────────────── */
  function drawWinLine(combo) {
    if (!winLine || !combo || combo.length < 2) return;

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

  function checkWinner(b) {
    for (const combo of WINNING_COMBOS) {
      const [a, b1, c1] = combo;
      if (b[a] && b[a] === b[b1] && b[a] === b[c1]) {
        return { winner: b[a], combo };
      }
    }
    return null;
  }

  /* ── Minimax AI ───────────────────────────────────── */
  function aiMove() {
    if (!active) return;
    const idx = bestMove();
    if (idx !== -1) makeMove(idx, current);
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
    active = true;
    current = 'X';
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
    scores = { X: 0, O: 0, draws: 0 };
    saveScores();
    renderStats();
  }

  /* ── Mode Toggle ──────────────────────────────────── */
  function setMode(m) {
    mode = m;
    modeBtns.forEach(btn => {
      if (btn.dataset.mode === m) btn.classList.add('active');
      else btn.classList.remove('active');
    });
    resetBoard();
  }

  /* ── Event Listeners ──────────────────────────────── */
  resetBtn.addEventListener('click', resetBoard);
  resetScoreBtn.addEventListener('click', resetAllScores);
  modeBtns.forEach(btn => {
    btn.addEventListener('click', () => setMode(btn.dataset.mode));
  });

  /* ── Init ──────────────────────────────────────────── */
  createBoard();
  renderStats();
})();
