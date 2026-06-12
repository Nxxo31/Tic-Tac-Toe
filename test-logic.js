// test-logic.js — Pure logic tests for triqui (no DOM needed)

const assert = require('assert');

// ── Inline game logic (same as app.js, refactored for testability) ──
const WINNING_COMBOS = [
  [0,1,2], [3,4,5], [6,7,8],
  [0,3,6], [1,4,7], [2,5,8],
  [0,4,8], [2,4,6]
];

function checkWinner(b) {
  for (const combo of WINNING_COMBOS) {
    const [a, b1, c1] = combo;
    if (b[a] && b[a] === b[b1] && b[a] === b[c1]) {
      return { winner: b[a], combo };
    }
  }
  return null;
}

function minimax(b, depth, isMax, alpha, beta, aiSymbol, humanSymbol) {
  const res = checkWinner(b);
  if (res) return res.winner === aiSymbol ? 10 - depth : depth - 10;
  if (b.every(c => c !== null)) return 0;

  if (isMax) {
    let maxEval = -Infinity;
    for (let i = 0; i < 9; i++) {
      if (!b[i]) {
        b[i] = aiSymbol;
        const ev = minimax(b, depth + 1, false, alpha, beta, aiSymbol, humanSymbol);
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
        const ev = minimax(b, depth + 1, true, alpha, beta, aiSymbol, humanSymbol);
        b[i] = null;
        minEval = Math.min(minEval, ev);
        beta = Math.min(beta, ev);
        if (beta <= alpha) break;
      }
    }
    return minEval;
  }
}

function bestMove(board, aiSymbol, humanSymbol) {
  let best = -1;
  let bestVal = -Infinity;
  for (let i = 0; i < 9; i++) {
    if (!board[i]) {
      board[i] = aiSymbol;
      const val = minimax(board, 0, false, -Infinity, Infinity, aiSymbol, humanSymbol);
      board[i] = null;
      if (val > bestVal) {
        bestVal = val;
        best = i;
      }
    }
  }
  return best;
}

// ── Tests ──
let passed = 0;
let failed = 0;

function test(name, fn) {
  try { fn(); console.log(`PASS  ${name}`); passed++; }
  catch (e) { console.log(`FAIL  ${name}: ${e.message}`); failed++; }
}

// 1. Empty board → best move should be center (4) or corner
test('Empty board best move is center or corner', () => {
  const board = Array(9).fill(null);
  const move = bestMove(board, 'O', 'X');
  assert([0, 2, 4, 6, 8].includes(move), `Got ${move}`);
});

// 2. AI blocks human win
test('AI blocks immediate loss', () => {
  const board = ['X','X',null, null,null,null, null,null,null];
  const move = bestMove(board, 'O', 'X');
  assert.strictEqual(move, 2, `Expected 2, got ${move}`);
});

// 3. AI takes win when possible
test('AI takes winning move', () => {
  const board = ['O','O',null, null,null,null, null,null,null];
  const move = bestMove(board, 'O', 'X');
  assert.strictEqual(move, 2, `Expected 2, got ${move}`);
});

// 4. Simulate games: AI never loses
test('AI never loses against random player (100 games)', () => {
  for (let g = 0; g < 100; g++) {
    let board = Array(9).fill(null);
    let current = 'X'; // Human
    let winner = null;
    while (!winner && board.some(c => c === null)) {
      if (current === 'X') {
        // Random valid move
        const empties = board.map((c, i) => c === null ? i : null).filter(i => i !== null);
        const move = empties[Math.floor(Math.random() * empties.length)];
        board[move] = 'X';
        const res = checkWinner(board);
        if (res) { winner = res.winner; break; }
        current = 'O';
      } else {
        const move = bestMove(board, 'O', 'X');
        board[move] = 'O';
        const res = checkWinner(board);
        if (res) { winner = res.winner; break; }
        current = 'X';
      }
    }
    if (winner === 'X') throw new Error('AI lost!');
  }
});

// 5. Draw scenario: AI vs perfect opponent (itself)
test('AI vs AI always draws', () => {
  let board = Array(9).fill(null);
  let current = 'X';
  let winner = null;
  while (!winner && board.some(c => c === null)) {
    const ai = current === 'X' ? 'X' : 'O';
    const human = current === 'X' ? 'O' : 'X';
    const move = bestMove(board, ai, human);
    board[move] = current;
    const res = checkWinner(board);
    if (res) { winner = res.winner; break; }
    current = current === 'X' ? 'O' : 'X';
  }
  if (winner !== null) throw new Error(`Should be draw, got winner ${winner}`);
});

console.log(`\nResults: ${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
