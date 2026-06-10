(function(){
  /* ── State ──────────────────────────────────────── */
  const N = 3;
  const WINNING_COMBOS = [
    [0,1,2],[3,4,5],[6,7,8],  // rows
    [0,3,6],[1,4,7],[2,5,8],  // cols
    [0,4,8],[2,4,6]           // diags
  ];

  let board     = Array(N * N).fill(null);
  let current   = 'X';               // 'X' or 'O'
  let gameOver  = false;
  let moves     = 0;

  let scores    = { X: 0, O: 0, draws: 0 };
  let winCells  = [];

  /* ── DOM refs ───────────────────────────────────── */
  const boardEl      = document.getElementById('board');
  const turnMark     = document.getElementById('turnMark');
  const turnIndicator= document.getElementById('turnIndicator');
  const statusMsg    = document.getElementById('statusMsg');
  const scoreXVal    = document.getElementById('scoreXVal');
  const scoreOVal    = document.getElementById('scoreOVal');
  const scoreDrawsVal= document.getElementById('scoreDrawsVal');
  const scoreXCard   = document.getElementById('scoreX');
  const scoreOCard   = document.getElementById('scoreO');
  const scoreDrawsCard= document.getElementById('scoreDraws');
  const resetBtn     = document.getElementById('resetBtn');
  const resetScoreBtn= document.getElementById('resetScoreBtn');

  /* ── Render helpers ─────────────────────────────── */
  function renderBoard() {
    boardEl.innerHTML = '';
    for (let i = 0; i < N * N; i++) {
      const cell = document.createElement('div');
      cell.className = 'cell';
      cell.dataset.idx = i;
      if (gameOver || board[i] !== null) cell.classList.add('taken');
      if (gameOver) cell.classList.add('game-over');

      if (board[i] !== null) {
        const span = document.createElement('span');
        span.textContent = board[i];
        span.className = 'pop';
        cell.appendChild(span);
      }

      // highlight win cells
      if (winCells.includes(i)) cell.classList.add('win');

      cell.addEventListener('click', () => handleClick(i));
      boardEl.appendChild(cell);
    }
  }

  function updateScores() {
    scoreXVal.textContent     = scores.X;
    scoreOVal.textContent     = scores.O;
    scoreDrawsVal.textContent = scores.draws;
  }

  function updateTurn() {
    if (gameOver) return;
    turnMark.textContent = current;
    turnMark.className = 'mark ' + (current === 'X' ? 'x' : 'o');

    // highlight active score card
    scoreXCard.classList.toggle('active', current === 'X');
    scoreOCard.classList.toggle('active', current === 'O');
    scoreDrawsCard.classList.remove('active');
  }

  function setStatus(text, type) {
    statusMsg.textContent = text;
    statusMsg.className = 'status-message' + (type ? ' ' + type : '');
  }

  function updateAll() {
    renderBoard();
    updateScores();
    updateTurn();
  }

  /* ── Game logic ─────────────────────────────────── */
  function checkWinner() {
    for (const combo of WINNING_COMBOS) {
      const [a,b,c] = combo;
      if (board[a] && board[a] === board[b] && board[a] === board[c]) {
        winCells = combo;
        return board[a];
      }
    }
    return null;
  }

  function handleClick(idx) {
    if (gameOver) return;
    if (board[idx] !== null) return;

    // place mark
    board[idx] = current;
    moves++;

    // check
    const winner = checkWinner();
    if (winner) {
      gameOver = true;
      scores[winner]++;
      const name = winner === 'X' ? 'X' : 'O';
      setStatus('¡' + name + ' gana! 🎉', 'win');
      updateAll();
      return;
    }

    if (moves === N * N) {
      // draw
      gameOver = true;
      scores.draws++;
      setStatus('¡Empate!', 'draw');
      updateAll();
      return;
    }

    // switch turn
    current = current === 'X' ? 'O' : 'X';
    updateAll();
  }

  function resetBoard() {
    board     = Array(N * N).fill(null);
    current   = 'X';
    gameOver  = false;
    moves     = 0;
    winCells  = [];
    setStatus('¡A jugar!');
    updateAll();
  }

  function resetScores() {
    scores = { X: 0, O: 0, draws: 0 };
    resetBoard();
  }

  /* ── Init ───────────────────────────────────────── */
  resetBtn.addEventListener('click', resetBoard);
  resetScoreBtn.addEventListener('click', resetScores);
  resetBoard();
})();
