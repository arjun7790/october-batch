
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EXTINCTION RUN | Dino Game</title>

<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Rajdhani:wght@400;500;700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    min-height: 100vh;
    overflow: hidden;
    background: #070910;
    color: white;
    font-family: 'Rajdhani', sans-serif;
}

.scene {
    position: relative;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    overflow: hidden;
    background:
        radial-gradient(ellipse at 50% 70%, #56251e 0%, transparent 48%),
        linear-gradient(180deg, #070a18 0%, #19182c 45%, #512b36 76%, #100c18 100%);
}

.scene::before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    opacity: .3;
    background-image:
        radial-gradient(1px 1px at 10% 20%, white 100%, transparent),
        radial-gradient(2px 2px at 75% 13%, white 100%, transparent),
        radial-gradient(1px 1px at 48% 32%, white 100%, transparent),
        radial-gradient(1px 1px at 88% 44%, white 100%, transparent),
        radial-gradient(2px 2px at 24% 42%, white 100%, transparent),
        radial-gradient(1px 1px at 63% 8%, white 100%, transparent),
        radial-gradient(1px 1px at 35% 12%, white 100%, transparent);
    background-size: 300px 200px;
}

.moon {
    position: absolute;
    top: 11%;
    right: 17%;
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: #ffddc2;
    box-shadow: 0 0 35px #ff996655, 0 0 100px #ff663322;
    opacity: .8;
}

.mountain {
    position: absolute;
    bottom: 25%;
    width: 120%;
    height: 200px;
    left: -10%;
    opacity: .45;
    background: #171522;
    clip-path: polygon(0 90%, 12% 55%, 23% 80%, 38% 25%,
    50% 76%, 67% 15%, 80% 72%, 91% 38%, 100% 75%, 100% 100%, 0 100%);
}

.mountain.back {
    bottom: 27%;
    transform: scaleX(-1) translateY(20px);
    opacity: .3;
    background: #292035;
}

.interface {
    position: relative;
    z-index: 2;
    width: min(1100px, 100%);
}

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 32px;
}

.brand {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(15px, 2.2vw, 23px);
    font-weight: 900;
    letter-spacing: 4px;
}

.brand span {
    color: #ff805b;
}

.status {
    font-size: 12px;
    letter-spacing: 3px;
    color: #c5c4d4;
    text-align: right;
}

.status i {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #ff805b;
    margin-right: 8px;
    box-shadow: 0 0 12px #ff805b;
}

.hero {
    text-align: center;
    margin-bottom: 24px;
}

.eyebrow {
    color: #ff9a78;
    letter-spacing: 6px;
    font-size: 11px;
    font-weight: 700;
    margin-bottom: 10px;
}

h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(34px, 6vw, 70px);
    font-weight: 900;
    letter-spacing: 4px;
    line-height: 1.15;
    text-shadow: 0 0 35px #ff6b4a25;
}

h1 span {
    color: #ff8865;
}

.subtitle {
    color: #c4b8c4;
    letter-spacing: 3px;
    font-size: 13px;
    margin-top: 12px;
}

.game-panel {
    position: relative;
    border: 1px solid #ffad8a38;
    border-radius: 14px;
    padding: 14px;
    background: linear-gradient(135deg, #171321dd, #100e1ceF);
    box-shadow: 0 25px 100px #0008, 0 0 35px #ff734b0c;
    backdrop-filter: blur(15px);
}

.hud {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 8px 14px;
    gap: 12px;
}

.hud-label {
    font-size: 10px;
    color: #aaa4bd;
    letter-spacing: 3px;
}

.hud-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 22px;
    color: #ffb18c;
    margin-top: 5px;
}

.best {
    text-align: right;
}

.canvas-wrap {
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    background: linear-gradient(180deg, #201b30, #452a39 68%, #191321);
}

canvas {
    display: block;
    width: 100%;
    height: auto;
    touch-action: manipulation;
}

.overlay {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: #0b0a14a8;
    backdrop-filter: blur(3px);
    padding: 20px;
}

.overlay.hidden {
    display: none;
}

.overlay-content h2 {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(24px, 4vw, 38px);
    letter-spacing: 3px;
    margin-bottom: 12px;
}

.overlay-content p {
    color: #d3c6d5;
    letter-spacing: 1px;
    margin-bottom: 22px;
}

button {
    border: 1px solid #ff9a79;
    color: #fff;
    background: linear-gradient(135deg, #ff805b, #c84743);
    padding: 13px 28px;
    border-radius: 4px;
    font-family: 'Orbitron', sans-serif;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    cursor: pointer;
    box-shadow: 0 0 28px #ff674a30;
    transition: transform .2s, box-shadow .2s;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 35px #ff674a70;
}

.bottom {
    display: flex;
    justify-content: space-between;
    gap: 15px;
    flex-wrap: wrap;
    margin-top: 18px;
    color: #c1b5c9;
    font-size: 12px;
    letter-spacing: 1px;
}

.key {
    display: inline-block;
    border: 1px solid #ffffff35;
    border-radius: 4px;
    padding: 4px 8px;
    margin: 0 3px;
    color: #fff;
    background: #ffffff0a;
}

.footer {
    text-align: center;
    margin-top: 24px;
    color: #777184;
    font-size: 10px;
    letter-spacing: 3px;
}

@media (max-width: 600px) {
    .scene { padding: 15px; }
    .topbar { margin-bottom: 24px; }
    .moon { width: 60px; height: 60px; right: 10%; }
    .game-panel { padding: 8px; }
    .bottom { font-size: 10px; }
    .brand { letter-spacing: 2px; }
    .status { letter-spacing: 1px; }
}
</style>
</head>

<body>
<div class="scene">
    <div class="moon"></div>
    <div class="mountain back"></div>
    <div class="mountain"></div>

    <main class="interface">
        <header class="topbar">
            <div class="brand">NO<span>INTERNET</span>.EXE</div>
            <div class="status"><i></i> OFFLINE WORLD / 001</div>
        </header>

        <section class="hero">
            <div class="eyebrow">A SURVIVAL EXPERIENCE</div>
            <h1>EXTINCTION <span>RUN</span></h1>
            <p class="subtitle">THE WORLD ENDED. YOUR RUN DIDN'T.</p>
        </section>

        <section class="game-panel">
            <div class="hud">
                <div>
                    <div class="hud-label">DISTANCE SCORE</div>
                    <div class="hud-value" id="score">00000</div>
                </div>
                <div class="best">
                    <div class="hud-label">PERSONAL BEST</div>
                    <div class="hud-value" id="best">00000</div>
                </div>
            </div>

            <div class="canvas-wrap">
                <canvas id="game" width="1000" height="350"></canvas>

                <div class="overlay" id="overlay">
                    <div class="overlay-content">
                        <h2 id="overlayTitle">THE RUN BEGINS</h2>
                        <p id="overlayText">Jump. Survive. Outrun extinction.</p>
                        <button id="startBtn">INITIALIZE RUN</button>
                    </div>
                </div>
            </div>
        </section>

        <div class="bottom">
            <div><span class="key">SPACE</span> / <span class="key">↑</span> JUMP</div>
            <div><span class="key">↓</span> DUCK</div>
            <div>PRESS ANYWHERE ON THE GAME TO JUMP</div>
        </div>

        <div class="footer">SYSTEM STATUS: OFFLINE &nbsp; // &nbsp; SURVIVAL IS EVERYTHING</div>
    </main>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const scoreEl = document.getElementById("score");
const bestEl = document.getElementById("best");
const overlay = document.getElementById("overlay");
const titleEl = document.getElementById("overlayTitle");
const textEl = document.getElementById("overlayText");
const startBtn = document.getElementById("startBtn");

const W = canvas.width;
const H = canvas.height;
const groundY = 282;

let running = false;
let gameOver = false;
let score = 0;
let best = 0;
let speed = 6;
let frame = 0;
let obstacles = [];
let particles = [];
let stars = [];
let lastTime = 0;
let spawnTimer = 0;
let ducking = false;

try {
    best = Number(localStorage.getItem("extinctionBest")) || 0;
} catch (e) {}
bestEl.textContent = String(best).padStart(5, "0");

const dino = {
    x: 110,
    y: groundY - 58,
    w: 48,
    h: 58,
    vy: 0,
    jumping: false
};

for (let i = 0; i < 70; i++) {
    stars.push({
        x: Math.random() * W,
        y: Math.random() * 220,
        size: Math.random() * 1.8 + .4,
        alpha: Math.random() * .7 + .2
    });
}

function resetGame() {
    score = 0;
    speed = 6;
    frame = 0;
    spawnTimer = 70;
    obstacles = [];
    particles = [];
    dino.y = groundY - dino.h;
    dino.vy = 0;
    dino.jumping = false;
    ducking = false;
    gameOver = false;
    running = true;
    overlay.classList.add("hidden");
    lastTime = performance.now();
}

function startGame() {
    if (running) return;
    resetGame();
}

startBtn.addEventListener("click", startGame);

function jump() {
    if (!running) {
        startGame();
        return;
    }

    if (!dino.jumping) {
        dino.vy = -15.5;
        dino.jumping = true;
        makeDust(dino.x + 12, groundY - 3, 8);
    }
}

function makeDust(x, y, count) {
    for (let i = 0; i < count; i++) {
        particles.push({
            x, y,
            vx: (Math.random() - .5) * 4,
            vy: -Math.random() * 3,
            life: 18 + Math.random() * 12,
            size: Math.random() * 4 + 1
        });
    }
}

document.addEventListener("keydown", e => {
    if (["Space", "ArrowUp", "ArrowDown"].includes(e.code)) {
        e.preventDefault();
    }

    if (e.code === "Space" || e.code === "ArrowUp" || e.code === "KeyW") {
        if (!e.repeat) jump();
    }

    if (e.code === "ArrowDown" || e.code === "KeyS") {
        ducking = true;
    }

    if (e.code === "Enter" && !running) startGame();
});

document.addEventListener("keyup", e => {
    if (e.code === "ArrowDown" || e.code === "KeyS") {
        ducking = false;
    }
});

canvas.addEventListener("pointerdown", () => {
    jump();
});

function drawBackground() {
    const sky = ctx.createLinearGradient(0, 0, 0, H);
    sky.addColorStop(0, "#17172b");
    sky.addColorStop(.65, "#4c2a3b");
    sky.addColorStop(1, "#1c1424");
    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, W, H);

    // Distant stars
    stars.forEach(s => {
        ctx.globalAlpha = s.alpha * (.7 + Math.sin(frame * .03 + s.x) * .3);
        ctx.fillStyle = "#ffe6d2";
        ctx.fillRect(s.x, s.y, s.size, s.size);
    });
    ctx.globalAlpha = 1;

    // Moon
    ctx.save();
    ctx.shadowBlur = 28;
    ctx.shadowColor = "#ffac84";
    ctx.fillStyle = "#f4c7b0";
    ctx.beginPath();
    ctx.arc(790, 85, 36, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    // Mountains
    drawMountain(0, 230, 150, "#332439", 0);
    drawMountain(300, 245, 110, "#281d30", 1);
    drawMountain(620, 230, 145, "#36233a", 2);
    drawMountain(830, 250, 100, "#251b2c", 3);

    // Distant ruins
    ctx.fillStyle = "#211a2b";
    for (let i = 0; i < 7; i++) {
        let x = ((i * 190 - frame * .5) % (W + 200) + W + 200) % (W + 200) - 100;
        ctx.fillRect(x, 223, 13, 60);
        ctx.fillRect(x - 7, 219, 27, 8);
        ctx.fillRect(x + 4, 238, 4, 18);
    }

    // Ground
    const ground = ctx.createLinearGradient(0, groundY, 0, H);
    ground.addColorStop(0, "#5c3542");
    ground.addColorStop(.1, "#2b1b2b");
    ground.addColorStop(1, "#17111f");
    ctx.fillStyle = ground;
    ctx.fillRect(0, groundY, W, H - groundY);

    ctx.save();
    ctx.shadowBlur = 14;
    ctx.shadowColor = "#ff815f";
    ctx.strokeStyle = "#ff9a79";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, groundY);
    ctx.lineTo(W, groundY);
    ctx.stroke();
    ctx.restore();

    // Moving ground markings
    ctx.strokeStyle = "#b66c7044";
    ctx.lineWidth = 2;
    for (let i = 0; i < 22; i++) {
        const x = ((i * 70 - frame * speed * .8) % (W + 70) + W + 70) % (W + 70);
        ctx.beginPath();
        ctx.moveTo(x, groundY + 20 + (i % 3) * 8);
        ctx.lineTo(x - 25, groundY + 20 + (i % 3) * 8);
        ctx.stroke();
    }
}

function drawMountain(x, base, height, color, offset) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(x - 80, base);
    ctx.lineTo(x + 70, base - height);
    ctx.lineTo(x + 160, base - 15);
    ctx.lineTo(x + 260, base - height * .6);
    ctx.lineTo(x + 380, base);
    ctx.closePath();
    ctx.fill();
}

function drawDino() {
    const x = dino.x;
    const h = ducking && !dino.jumping ? 35 : dino.h;
    const y = groundY - h;

    ctx.save();
    ctx.shadowBlur = 14;
    ctx.shadowColor = "#ff8b69";
    ctx.fillStyle = "#ff9a78";

    // Tail
    ctx.beginPath();
    ctx.moveTo(x + 9, y + 32);
    ctx.lineTo(x - 13, y + 42);
    ctx.lineTo(x + 10, y + 43);
    ctx.closePath();
    ctx.fill();

    if (ducking && !dino.jumping) {
        ctx.fillRect(x + 8, y + 15, 35, 19);
        ctx.fillRect(x + 30, y + 4, 22, 20);
    } else {
        // Body
        ctx.fillRect(x + 9, y + 25, 29, 24);
        // Head
        ctx.fillRect(x + 25, y + 4, 26, 27);
        // Snout
        ctx.fillRect(x + 39, y + 16, 15, 10);
        // Back spikes
        ctx.beginPath();
        ctx.moveTo(x + 11, y + 26);
        ctx.lineTo(x + 15, y + 17);
        ctx.lineTo(x + 21, y + 26);
        ctx.lineTo(x + 26, y + 16);
        ctx.lineTo(x + 31, y + 27);
        ctx.closePath();
        ctx.fill();
    }

    ctx.shadowBlur = 0;

    // Eye
    ctx.fillStyle = "#201426";
    ctx.fillRect(x + 41, y + 9, 4, 4);

    // Legs animate while running
    const step = running && !dino.jumping ? Math.floor(frame / 5) % 2 : 0;
    ctx.fillStyle = "#f6c0a2";
    if (!dino.jumping) {
        ctx.fillRect(x + 14, groundY - 14, 8, 14);
        ctx.fillRect(x + 29, groundY - 14, 8, 14);
        if (step) {
            ctx.clearRect(x + 12, groundY - 5, 30, 5);
            ctx.fillRect(x + 10, groundY - 11, 9, 11);
            ctx.fillRect(x + 31, groundY - 15, 8, 15);
        }
    } else {
        ctx.fillRect(x + 14, y + 45, 8, 13);
        ctx.fillRect(x + 30, y + 45, 8, 13);
    }

    ctx.restore();
}

function spawnObstacle() {
    const bird = score > 180 && Math.random() < .28;
    if (bird) {
        obstacles.push({
            type: "bird",
            x: W + 20,
            y: groundY - 65 - Math.random() * 35,
            w: 42,
            h: 25,
            wing: 0
        });
    } else {
        const tall = Math.random() < .45;
        obstacles.push({
            type: "cactus",
            x: W + 20,
            y: groundY - (tall ? 57 : 39),
            w: tall ? 26 : 20,
            h: tall ? 57 : 39
        });
    }
}

function drawObstacle(o) {
    ctx.save();
    ctx.shadowBlur = 10;
    ctx.shadowColor = "#ff765b";

    if (o.type === "cactus") {
        ctx.fillStyle = "#83b18b";
        ctx.fillRect(o.x + 7, o.y, 12, o.h);
        ctx.fillRect(o.x, o.y + 15, 9, 7);
        ctx.fillRect(o.x, o.y + 9, 6, 13);
        ctx.fillRect(o.x + 18, o.y + 21, 8, 7);
        ctx.fillRect(o.x + 20, o.y + 14, 6, 14);
        ctx.fillRect(o.x + 4, o.y + o.h - 5, 18, 5);
    } else {
        const wingY = Math.sin(frame * .35) * 7;
        ctx.fillStyle = "#e2a8a1";
        ctx.beginPath();
        ctx.ellipse(o.x + 21, o.y + 12, 19, 7, 0, 0, Math.PI * 2);
        ctx.fill();

        ctx.beginPath();
        ctx.moveTo(o.x + 22, o.y + 13);
        ctx.lineTo(o.x + 12, o.y + wingY);
        ctx.lineTo(o.x + 27, o.y + 8);
        ctx.fill();

        ctx.fillStyle = "#201426";
        ctx.fillRect(o.x + 31, o.y + 9, 3, 3);
    }

    ctx.restore();
}

function updateParticles() {
    particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        p.vy += .13;
        p.life--;
        ctx.globalAlpha = Math.max(0, p.life / 30);
        ctx.fillStyle = "#ffad83";
        ctx.fillRect(p.x, p.y, p.size, p.size);
    });
    ctx.globalAlpha = 1;
    particles = particles.filter(p => p.life > 0);
}

function checkCollision(o) {
    const dx = dino.x + 11;
    const dy = dino.y + 8;
    const dw = dino.w - 15;
    const dh = dino.h - 12;

    const ox = o.x + 3;
    const oy = o.y + 3;
    const ow = o.w - 6;
    const oh = o.h - 4;

    return dx < ox + ow &&
           dx + dw > ox &&
           dy < oy + oh &&
           dy + dh > oy;
}

function endGame() {
    running = false;
    gameOver = true;

    if (score > best) {
        best = score;
        try {
            localStorage.setItem("extinctionBest", best);
        } catch (e) {}
    }

    bestEl.textContent = String(best).padStart(5, "0");
    titleEl.textContent = "RUN TERMINATED";
    textEl.textContent = "Distance survived: " + score + " points";
    startBtn.textContent = "RESTART MISSION";
    overlay.classList.remove("hidden");
    makeDust(dino.x + 20, groundY - 5, 18);
}

function update(dt) {
    if (!running) return;

    frame += dt;
    score += dt * speed * .075;
    speed = Math.min(13, 6 + score / 250);
    scoreEl.textContent = String(Math.floor(score)).padStart(5, "0");

    // Gravity and jumping
    dino.vy += .75 * dt;
    dino.y += dino.vy * dt;

    if (dino.y >= groundY - dino.h) {
        dino.y = groundY - dino.h;
        dino.vy = 0;
        dino.jumping = false;
    }

    spawnTimer -= dt;
    if (spawnTimer <= 0) {
        spawnObstacle();
        spawnTimer = Math.max(42, 90 + Math.random() * 65 - speed * 3);
    }

    obstacles.forEach(o => {
        o.x -= speed * dt;
        if (checkCollision(o)) {
            endGame();
        }
    });

    obstacles = obstacles.filter(o => o.x + o.w > -20);
}

function draw() {
    drawBackground();

    obstacles.forEach(drawObstacle);
    drawDino();
    updateParticles();

    if (running) {
        ctx.fillStyle = "#ffb18c";
        ctx.font = "12px monospace";
        ctx.fillText("SURVIVE", W - 100, 28);
    }
}

function loop(now) {
    const dt = Math.min((now - lastTime) / 16.67 || 1, 2);
    lastTime = now;

    update(dt);
    draw();
    requestAnimationFrame(loop);
}

draw();
requestAnimationFrame(loop);
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)
