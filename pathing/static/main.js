const rows = 20;
const cols = 20;
let start = null;
let end = null;
let grid = Array.from({ length: rows }, () => Array(cols).fill(0));

const gridEl = document.getElementById("grid");
gridEl.style.gridTemplateRows = `repeat(${rows}, 20px)`;
gridEl.style.gridTemplateColumns = `repeat(${cols}, 20px)`;

let isMouseDown = false;
let drawMode = null; // 'add' or 'remove'
let mode = 'setStart'; // 'setStart' -> 'setEnd' -> 'draw'

function resetGridStyles() {
    document.querySelectorAll(".cell").forEach(cell => {
        cell.classList.remove("start", "end", "wall", "visited", "path");
    });
}

resetGridStyles();

// Create grid cells
for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
        const cell = document.createElement("div");
        cell.className = "cell";
        cell.dataset.row = r;
        cell.dataset.col = c;

        cell.addEventListener("mousedown", (e) => {
            if (mode === 'setStart') {
                start = [r, c];
                cell.classList.add("start");
                mode = 'setEnd';
                console.log("Start set at:", start);
            } else if (mode === 'setEnd') {
                if (start && r === start[0] && c === start[1]) return;
                end = [r, c];
                cell.classList.add("end");
                mode = 'draw';
                console.log("End set at:", end);
            } else if (mode === 'draw') {
                if (start && r === start[0] && c === start[1]) return;
                if (end && r === end[0] && c === end[1]) return;
                isMouseDown = true;
                if (grid[r][c] === 0) {
                    grid[r][c] = 1;
                    cell.classList.add("wall");
                    drawMode = "add";
                } else {
                    grid[r][c] = 0;
                    cell.classList.remove("wall");
                    drawMode = "remove";
                }
            }
        });

        cell.addEventListener("mouseenter", (e) => {
            if (!isMouseDown || mode !== 'draw') return;
            if (start && r === start[0] && c === start[1]) return;
            if (end && r === end[0] && c === end[1]) return;
            if (drawMode === "add") {
                grid[r][c] = 1;
                cell.classList.add("wall");
            } else if (drawMode === "remove") {
                grid[r][c] = 0;
                cell.classList.remove("wall");
            }
        });

        gridEl.appendChild(cell);
    }
}

document.body.addEventListener("mouseup", () => {
    isMouseDown = false;
    drawMode = null;
});

// Solve button handler
async function solve() {
  if (!start || !end) {
    alert("Please set both start and end points first.");
    return;
  }

  const algorithm = document.getElementById("algorithm").value;
  const speed = document.getElementById("speed").value;

  const startTime = performance.now();

  const response = await fetch("/solve", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ grid, start, end, algorithm })
  });

  const endTime = performance.now();
  const elapsedTime = (endTime - startTime).toFixed(2);

  const data = await response.json();

  // Clear previous styles
  document.querySelectorAll(".cell").forEach(cell => {
    cell.classList.remove("visited", "path");
  });

  // Recolor start/end
  if (start) {
    const index = start[0] * cols + start[1];
    gridEl.children[index].classList.add("start");
  }
  if (end) {
    const index = end[0] * cols + end[1];
    gridEl.children[index].classList.add("end");
  }

  // Compute delay
  let totalDuration = 2000; // base 2 seconds
  if (speed === "slow") totalDuration = 4000;
  else if (speed === "fast") totalDuration = 1000;
  else if (speed === "instant") totalDuration = 0;

  const numSteps = data.expanded.length;
  const delay = numSteps > 0 ? Math.floor(totalDuration / numSteps) : 0;

  // Animate expanded nodes
  for (let [r, c] of data.expanded) {
    if ((r === start[0] && c === start[1]) || (r === end[0] && c === end[1])) continue;
    const index = r * cols + c;
    gridEl.children[index].classList.add("visited");
    if (delay > 0) {
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  // Show final path
  data.path.forEach(([r, c]) => {
    if ((r === start[0] && c === start[1]) || (r === end[0] && c === end[1])) return;
    const index = r * cols + c;
    gridEl.children[index].classList.add("path");
  });

  // Show notification
  const notif = document.getElementById("notification");
  notif.textContent = `Expanded ${numSteps} nodes in ${elapsedTime} ms using ${algorithm.toUpperCase()}.`;
}


function generateMaze() {
  if (!start || !end) {
    alert("Please set both start and end points first.");
    return;
  }

  // Clear all walls and paths
  document.querySelectorAll(".cell").forEach(cell => {
    cell.classList.remove("wall", "visited", "path");
  });

  // Reset grid array
  grid = Array.from({ length: rows }, () => Array(cols).fill(0));

  // Randomly set walls
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      // Skip start/end cells
      if ((r === start[0] && c === start[1]) || (r === end[0] && c === end[1])) continue;

      if (Math.random() < 0.3) { // 30% chance to be a wall
        grid[r][c] = 1;
        const index = r * cols + c;
        gridEl.children[index].classList.add("wall");
      }
    }
  }

  // Clear any notification
  document.getElementById("notification").textContent = "";
}


function resetGrid() {
    // Clear styles
    document.querySelectorAll(".cell").forEach(cell => {
        cell.classList.remove("start", "end", "wall", "visited", "path");
    });

    // Reset grid state
    grid = Array.from({ length: rows }, () => Array(cols).fill(0));

    // Reset start/end and mode
    start = null;
    end = null;
    mode = 'setStart';
    document.getElementById("notification").textContent = "";

}



