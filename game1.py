
from flask import Flask, render_template_string

app = Flask(__name__)

GAME = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LAST LIGHT — Dino Runner</title>

<style>
* { box-sizing: border-box; }

:root {
    --cyan: #55dfff;
    --gold: #ffc45c;
    --panel: rgba(4, 12, 28, .78);
}

body {
    margin: 0;
    min-height: 100vh;
    background: #030815;
    color: #e9f8ff;
    font-family: "Courier New", monospace;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 18px;
}

.game-shell {
    width: min(1200px, 100%);
    border: 1px solid #24658c;
    border-radius: 15px;
    overflow: hidden;
    background: #071326;
    box-shadow: 0 0 35px #008bff25, 0 0 100px #000;
}

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    padding: 15px 20px;
    background: #071020;
    border-bottom: 1px solid #1e4261;
    flex-wrap: wrap;
}

.brand {
    font-size: 20px;
    font-weight: bold;
    letter-spacing: 3px;
    color: var(--cyan);
    text-shadow: 0 0 14px #00bfff80;
}

.brand small {
    display: block;
    font-size: 10px;
    color: #91a8c1;
    margin-top: 5px;
    letter-spacing: 2px;
}

.hud {
    display: flex;
    gap: 20px;
    font-size: 12px;
    color: #9cb9d8;
}

.hud strong {
    display: block;
    margin-top: 4px;
    font-size: 22px;
    color: white;
}

.power {
    color: #55ffbd;
    border: 1px solid #228b74;
    border-radius: 20px;
    padding: 9px 13px;
    font-size: 12px;
    background: #0a292a;
}

.power.off {
    color: #ff7777;
    border-color: #b53649;
    background: #300e21;
}

.stage {
    position: relative;
    background: #111c3c;
}

canvas {
    display: block;
    width: 100%;
    height: auto;
    aspect-ratio: 16 / 7;
    outline: none;
    touch-action: manipulation;
}

.overlay {
    position: absolute;
    inset: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(1, 5, 17, .42);
    padding: 15px;
}

.overlay.hidden { display: none; }

.modal {
    width: min(400px, 95%);
    padding: 26px;
    text-align: center;
    background: rgba(3, 11, 27, .94);
    border: 1px solid var(--cyan);
    box-shadow: 0 0 35px #008cff30, inset 0 0 25px #008cff0c;
    border-radius: 12px;
}

.eyebrow {
    color: var(--gold);
    font-size: 11px;
    letter-spacing: 3px;
}

.modal h1 {
    font-size: clamp(25px, 5vw, 38px);
    margin: 13px 0;
    color: white;
    text-shadow: 0 0 15px #42baff;
}

.modal p {
    color: #a8c4df;
    line-height: 1.7;
    font-size: 13px;
}

button {
    border: 1px solid #70e4ff;
    border-radius: 6px;
    background: linear-gradient(110deg, #064e91, #087cbe);
    color: white;
    padding: 13px 20px;
    font: bold 13px "Courier New", monospace;
    cursor: pointer;
    letter-spacing: 1px;
}

button:hover {
    filter: brightness(1.3);
    box-shadow: 0 0 20px #00bfff50;
}

.controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 14px;
    padding: 15px 20px;
    flex-wrap: wrap;
    background: #071020;
}

.instructions {
    color: #9bb5d1;
    font-size: 11px;
    line-height: 1.9;
}

.instructions b { color: #d8f5ff; }

.actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.actions button {
    padding: 10px 12px;
    font-size: 11px;
}

.footer {
    padding: 10px;
    text-align: center;
    color: #536f8e;
    font-size: 10px;
    border-top: 1px solid #18304a;
    letter-spacing: 2px;
}

@media (max-width: 600px) {
    body { padding: 5px; }
    .topbar { padding: 12px; }
    .brand { font-size: 16px; }
    .hud { gap: 12px; }
    .hud strong { font-size: 17px; }
    .controls { padding: 12px; }
    .instructions { font-size: 10px; }
    .modal { padding: 17px; }
}
</style>
</head>

<body>
<div class="game-shell">

    <header class="topbar">
        <div class="brand">
            LAST LIGHT
            <small>AN ENDLESS SURVIVAL RUN</small>
        </div>

        <div class="hud">
            <div>SCORE<strong id="score">00000</strong></div>
            <div>BEST<strong id="best">00000</strong></div>
        </div>

        <div class="power" id="power">⚡ POWER: ON</div>
    </header>

    <div class="stage">
        <canvas id="game" width="1200" height="525"
                tabindex="0" aria-label="Dinosaur running game"></canvas>

        <div class="overlay" id="overlay">
            <div class="modal">
                <div class="eyebrow" id="eyebrow">MISSION 001 / SURVIVAL</div>
                <h1 id="title">LAST LIGHT</h1>
                <p id="description">
                    The world is fading. The run begins now.<br>
                    Jump over the ruins. Survive the darkness.
                </p>
                <button id="start">▶ START RUN</button>
                <p>SPACE / ↑ TO JUMP · ↓ TO DUCK</p>
            </div>
        </div>
    </div>

    <section class="controls">
        <div class="instructions">
            <b>SPACE / ↑ / TAP</b> — JUMP<br>
            <b>↓ / HOLD TOUCH</b> — DUCK<br>
            <b>P</b> — PAUSE &nbsp; <b>R</b> — RESTART
        </div>

        <div class="actions">
            <button id="pause">Ⅱ PAUSE</button>
            <button id="restart">↻ RESTART</button>
            <button id="powerButton">⚡ POWER TEST</button>
        </div>
    </section>

    <div class="footer">
        KEEP RUNNING · CHASE THE LAST LIGHT
    </div>
</div>

<script>
(() => {
    const canvas = document.getElementById("game");
    const ctx = canvas.getContext("2d");

    const $ = id => document.getElementById(id);
    const W = canvas.width;
    const H = canvas.height;
    const ground = 415;

    let running = false;
    let paused = false;
    let dead = false;
    let started = false;
    let powerOn = true;
    let score = 0;
    let best = 0;
    let speed = 340;
    let elapsed = 0;
    let spawnTimer = 1;
    let coinTimer = 2;
    let powerTimer = 0;
    let battery = 0;
    let lastTime = 0;
    let frame = 0;
    let obstacles = [];
    let coins = [];
    let particles = [];
    let stars = [];
    let audioContext = null;

    const dino = {
        x: 115, y: ground, vy: 0,
        width: 43, height: 49,
        ducking: false,
        jumping: false
    };

    let highScore = 0;
    try {
        highScore = Number(localStorage.getItem("lastLightBest") || 0);
    } catch (e) {}

    best = highScore;

    for (let i = 0; i < 100; i++) {
        stars.push({
            x: Math.random() * W,
            y: Math.random() * 300,
            r: Math.random() * 1.7 + .3,
            phase: Math.random() * 6
        });
    }

    function beep(freq = 500, duration = .08, type = "sine") {
        try {
            if (!audioContext) {
                audioContext = new (
                    window.AudioContext || window.webkitAudioContext
                )();
            }
            if (audioContext.state === "suspended") {
                audioContext.resume();
            }

            const oscillator = audioContext.createOscillator();
            const gain = audioContext.createGain();

            oscillator.type = type;
            oscillator.frequency.value = freq;
            gain.gain.setValueAtTime(.05, audioContext.currentTime);
            gain.gain.exponentialRampToValueAtTime(
                .001, audioContext.currentTime + duration
            );

            oscillator.connect(gain);
            gain.connect(audioContext.destination);
            oscillator.start();
            oscillator.stop(audioContext.currentTime + duration);
        } catch (e) {}
    }

    function updateHUD() {
        $("score").textContent = String(Math.floor(score)).padStart(5, "0");
        $("best").textContent = String(best).padStart(5, "0");
        $("power").textContent = powerOn
            ? "⚡ POWER: ON"
            : "⚡ POWER: OFF";
        $("power").classList.toggle("off", !powerOn);
        $("pause").textContent = paused ? "▶ RESUME" : "Ⅱ PAUSE";
        $("powerButton").textContent = powerOn
            ? "⚡ POWER TEST"
            : "🔋 RESTORE POWER";
    }

    function showOverlay(title, description, button, eyebrow) {
        $("title").textContent = title;
        $("description").innerHTML = description;
        $("start").textContent = button;
        $("eyebrow").textContent = eyebrow;
        $("overlay").classList.remove("hidden");
    }

    function hideOverlay() {
        $("overlay").classList.add("hidden");
    }

    function startGame() {
        score = 0;
        speed = 340;
        elapsed = 0;
        spawnTimer = 1.2;
        coinTimer = 1.6;
        powerTimer = 0;
        battery = 0;
        obstacles = [];
        coins = [];
        particles = [];
        dino.y = ground;
        dino.vy = 0;
        dino.jumping = false;
        dino.ducking = false;
        dead = false;
        paused = false;
        running = true;
        started = true;
        powerOn = true;
        lastTime = performance.now();
        hideOverlay();
        updateHUD();
        beep(650, .12);
        canvas.focus();
    }

    function gameOver() {
        if (dead) return;

        dead = true;
        running = false;
        dino.ducking = false;

        const finalScore = Math.floor(score);
        if (finalScore > best) {
            best = finalScore;
            try {
                localStorage.setItem("lastLightBest", String(best));
            } catch (e) {}
        }

        updateHUD();
        beep(150, .35, "sawtooth");

        showOverlay(
            "GAME OVER",
            "DISTANCE: " + finalScore +
            "<br>BEST DISTANCE: " + best +
            "<br><br>The desert remembers every run.",
            "↻ RUN AGAIN",
            "MISSION FAILED / TRY AGAIN"
        );
    }

    function jump() {
        if (!started || dead) {
            startGame();
            return;
        }

        if (paused || !running) return;

        if (dino.y >= ground - .5) {
            dino.vy = -730;
            dino.jumping = true;
            dino.ducking = false;
            beep(420, .07);
        }
    }

    function spawnObstacle() {
        const isBird = score > 60 && Math.random() < .30;

        if (isBird) {
            const birdY = Math.random() < .5 ? 325 : 365;
            obstacles.push({
                type: "bird",
                x: W + 30,
                y: birdY,
                w: 46,
                h: 25,
                phase: Math.random() * 5
            });
        } else {
            const tall = Math.random() < .30;
            obstacles.push({
                type: "cactus",
                x: W + 30,
                y: ground,
                w: tall ? 31 : 24,
                h: tall ? 68 : 44,
                variant: Math.floor(Math.random() * 3)
            });
        }
    }

    function spawnCoin() {
        const y = 285 + Math.random() * 70;
        for (let i = 0; i < 4; i++) {
            coins.push({
                x: W + 20 + i * 43,
                y: y + Math.sin(i * 1.2) * 12,
                r: 9,
                phase: i
            });
        }
    }

    function burst(x, y, color, count = 12) {
        for (let i = 0; i < count; i++) {
            const angle = Math.random() * Math.PI * 2;
            const velocity = 50 + Math.random() * 220;
            particles.push({
                x, y,
                vx: Math.cos(angle) * velocity,
                vy: Math.sin(angle) * velocity,
                life: .35 + Math.random() * .5,
                max: .85,
                color
            });
        }
    }

    function intersects(a, b) {
        return a.x < b.x + b.w &&
               a.x + a.w > b.x &&
               a.y < b.y + b.h &&
               a.y + a.h > b.y;
    }

    function update(dt) {
        if (!running || paused) return;

        elapsed += dt;
        frame += dt;
        score += dt * (powerOn ? 10 : 7);
        speed = Math.min(720, 340 + score * .8);

        dino.vy += 1850 * dt;
        dino.y += dino.vy * dt;

        if (dino.y >= ground) {
            dino.y = ground;
            dino.vy = 0;
            dino.jumping = false;
        }

        spawnTimer -= dt;
        if (spawnTimer <= 0) {
            spawnObstacle();
            spawnTimer = Math.max(
                .66, 1.25 + Math.random() * .7 - score / 2000
            );
        }

        coinTimer -= dt;
        if (coinTimer <= 0) {
            spawnCoin();
            coinTimer = 2.4 + Math.random() * 2.2;
        }

        if (!powerOn) {
            powerTimer += dt;
            if (powerTimer > 12) {
                powerTimer = 0;
                battery++;
                burst(1000, 90, "#57eaff", 18);
                beep(800, .15);
            }
        }

        const hitbox = {
            x: dino.x + 7,
            y: dino.y - (dino.ducking ? 25 : 44),
            w: dino.ducking ? 49 : 33,
            h: dino.ducking ? 24 : 40
        };

        obstacles.forEach(obstacle => {
            obstacle.x -= speed * dt;
            if (obstacle.type === "bird") {
                obstacle.phase += dt * 9;
            }

            const box = obstacle.type === "bird"
                ? {
                    x: obstacle.x + 4,
                    y: obstacle.y - 6,
                    w: obstacle.w - 8,
                    h: obstacle.h
                }
                : {
                    x: obstacle.x + 4,
                    y: obstacle.y - obstacle.h + 6,
                    w: obstacle.w - 8,
                    h: obstacle.h - 6
                };

            if (intersects(hitbox, box)) {
                gameOver();
            }
        });

        obstacles = obstacles.filter(o => o.x + o.w > -10);

        coins.forEach(coin => {
            coin.x -= speed * dt;
            coin.phase += dt * 5;

            const box = {
                x: coin.x - coin.r,
                y: coin.y - coin.r,
                w: coin.r * 2,
                h: coin.r * 2
            };

            if (!coin.taken && intersects(hitbox, box)) {
                coin.taken = true;
                score += 25;
                burst(coin.x, coin.y, "#ffc45c", 9);
                beep(900, .07);
            }
        });

        coins = coins.filter(c => c.x > -30 && !c.taken);

        particles.forEach(p => {
            p.x += p.vx * dt;
            p.y += p.vy * dt;
            p.vy += 180 * dt;
            p.life -= dt;
        });

        particles = particles.filter(p => p.life > 0);

        updateHUD();
    }

    function polygon(points, fill) {
        ctx.fillStyle = fill;
        ctx.beginPath();
        ctx.moveTo(points[0][0], points[0][1]);
        for (let i = 1; i < points.length; i++) {
            ctx.lineTo(points[i][0], points[i][1]);
        }
        ctx.closePath();
        ctx.fill();
    }

    function drawBackground() {
        const sky = ctx.createLinearGradient(0, 0, 0, H);
        sky.addColorStop(0, powerOn ? "#101d42" : "#02040d");
        sky.addColorStop(.52, powerOn ? "#81455b" : "#100c20");
        sky.addColorStop(1, "#10172c");
        ctx.fillStyle = sky;
        ctx.fillRect(0, 0, W, H);

        stars.forEach(s => {
            ctx.globalAlpha = .3 + .7 * Math.abs(
                Math.sin(frame * 1.4 + s.phase)
            );
            ctx.fillStyle = "#c7e9ff";
            ctx.fillRect(s.x, s.y, s.r, s.r);
        });
        ctx.globalAlpha = 1;

        const sunX = 850;
        const sunY = 220;
        const sunGlow = ctx.createRadialGradient(
            sunX, sunY, 4, sunX, sunY, 190
        );
        sunGlow.addColorStop(0, powerOn ? "#ffdc8c90" : "#0b1b3a40");
        sunGlow.addColorStop(1, "#ff704000");
        ctx.fillStyle = sunGlow;
        ctx.fillRect(sunX - 200, sunY - 200, 400, 400);

        ctx.beginPath();
        ctx.arc(sunX, sunY, 62, 0, Math.PI * 2);
        ctx.fillStyle = powerOn ? "#ffd17d" : "#1b2949";
        ctx.fill();

        // Distant mountains
        const shift1 = (elapsed * 10) % 180;
        for (let layer = 0; layer < 2; layer++) {
            const y = layer === 0 ? 300 : 340;
            const offset = layer === 0 ? shift1 : shift1 * 1.8;

            ctx.beginPath();
            ctx.moveTo(0, H);
            for (let x = -200; x <= W + 200; x += 60) {
                const peak = y - Math.abs(
                    Math.sin((x + offset) * .012 + layer)
                ) * (80 + layer * 20);
                ctx.lineTo(x, peak);
            }
            ctx.lineTo(W, H);
            ctx.closePath();
            ctx.fillStyle = layer === 0 ? "#272c50" : "#171e37";
            ctx.fill();
        }

        // Ruined futuristic buildings
        for (let i = 0; i < 15; i++) {
            const bw = 30 + (i % 4) * 13;
            const bx = ((i * 109 - elapsed * 35) % (W + 150)
                + W + 150) % (W + 150) - 60;
            const bh = 40 + ((i * 17) % 85);

            ctx.fillStyle = "#0b152b";
            ctx.fillRect(bx, ground - bh, bw, bh);

            ctx.fillStyle = powerOn ? "#fc8e6435" : "#2356a030";
            for (let wy = ground - bh + 12; wy < ground - 8; wy += 14) {
                ctx.fillRect(bx + 7, wy, 4, 5);
                ctx.fillRect(bx + bw - 12, wy, 4, 5);
            }
        }

        // Ground
        ctx.fillStyle = "#080e1e";
        ctx.fillRect(0, ground, W, H - ground);

        ctx.fillStyle = powerOn ? "#ffad70" : "#367ca4";
        ctx.fillRect(0, ground, W, 3);

        for (let i = 0; i < 70; i++) {
            const x = ((i * 73 - elapsed * speed * .4) % W + W) % W;
            const y = ground + 12 + (i * 19) % 100;
            ctx.fillStyle = i % 3 ? "#172743" : "#29334b";
            ctx.fillRect(x, y, 8 + i % 15, 2);
        }

        // Ground markings
        for (let i = 0; i < 25; i++) {
            const x = ((i * 65 - elapsed * speed) % W + W) % W;
            ctx.fillStyle = powerOn ? "#e6a76c" : "#3375a1";
            ctx.fillRect(x, ground + 14, 18, 2);
        }

        // Lightning in outage mode
        if (!powerOn) {
            ctx.globalAlpha = .6 + Math.sin(frame * 4) * .3;
            polygon([
                [1030, 90], [1005, 140], [1027, 137],
                [1010, 185], [1050, 125], [1029, 129]
            ], "#58caff");
            ctx.globalAlpha = 1;
        }
    }

    function drawDino() {
        const x = dino.x;
        const bottom = dino.y;
        const duck = dino.ducking && !dino.jumping;
        const bob = !dino.jumping ? Math.sin(frame * 16) * 2 : 0;

        ctx.save();
        ctx.translate(x, bottom + bob);

        // Scarf
        ctx.fillStyle = "#ff5e60";
        ctx.beginPath();
        ctx.moveTo(15, -34);
        ctx.lineTo(-5 - Math.sin(frame * 10) * 8, -26);
        ctx.lineTo(11, -25);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = powerOn ? "#9af2e2" : "#75c8ff";

        if (duck) {
            ctx.fillRect(0, -24, 47, 19);
            ctx.fillRect(25, -36, 23, 18);
            ctx.fillRect(42, -32, 12, 10);
            ctx.fillStyle = "#071020";
            ctx.fillRect(40, -31, 4, 4);
        } else {
            // Tail
            polygon([[7,-22],[-7,-16],[4,-11]], "#5bd6c4");

            // Body
            ctx.fillRect(5, -33, 27, 24);
            ctx.fillRect(16, -45, 13, 18);

            // Head
            ctx.fillRect(18, -56, 29, 25);
            ctx.fillRect(36, -46, 17, 13);

            // Spikes
            polygon([[18,-54],[20,-62],[25,-54]], "#5bd6c4");
            polygon([[28,-54],[31,-62],[35,-54]], "#5bd6c4");

            // Eye
            ctx.fillStyle = "#071020";
            ctx.fillRect(39, -50, 5, 5);
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(40, -50, 2, 2);

            // Legs
            const leg = Math.sin(frame * 20) * 5;
            if (!dino.jumping) {
                ctx.fillStyle = "#4bb8b2";
                ctx.fillRect(9, -12, 8, 12 + leg);
                ctx.fillRect(25, -12, 8, 12 - leg);
            } else {
                ctx.fillRect(8, -12, 8, 12);
                ctx.fillRect(25, -12, 8, 12);
            }
        }

        ctx.restore();
    }

    function drawCactus(o) {
        const x = o.x;
        const bottom = o.y;
        const h = o.h;

        ctx.save();
        ctx.translate(x, bottom);

        ctx.shadowColor = "#43ffab";
        ctx.shadowBlur = 9;
        ctx.fillStyle = "#32c984";

        ctx.fillRect(o.w * .36, -h, o.w * .32, h);
        ctx.fillRect(0, -h * .64, o.w * .35, 8);
        ctx.fillRect(0, -h * .64, 7, h * .30);
        ctx.fillRect(o.w * .65, -h * .42, o.w * .35, 8);
        ctx.fillRect(o.w * .65, -h * .42, 7, h * .22);

        ctx.shadowBlur = 0;
        ctx.fillStyle = "#a0ffd0";
        ctx.fillRect(o.w * .43, -h + 5, 2, h * .25);

        ctx.restore();
    }

    function drawBird(o) {
        const flap = Math.sin(o.phase) * 11;

        ctx.save();
        ctx.translate(o.x, o.y);
        ctx.fillStyle = "#171629";
        ctx.shadowColor = "#ff9e6a";
        ctx.shadowBlur = 5;

        ctx.fillRect(13, 9, 24, 8);
        ctx.fillRect(31, 6, 11, 8);

        polygon([
            [18, 11], [3, flap], [11, flap + 15], [24, 14]
        ], "#f7a66d");

        polygon([
            [25, 11], [39, -flap], [36, -flap + 14], [27, 14]
        ], "#f7a66d");

        ctx.fillRect(40, 7, 7, 3);
        ctx.restore();
    }

    function drawCoins() {
        coins.forEach(c => {
            const pulse = 1 + Math.sin(c.phase) * .12;

            ctx.save();
            ctx.translate(c.x, c.y);
            ctx.scale(pulse, 1);

            ctx.shadowColor = "#ffc45c";
            ctx.shadowBlur = 15;
            ctx.fillStyle = "#ffc45c";
            ctx.beginPath();
            ctx.arc(0, 0, c.r, 0, Math.PI * 2);
            ctx.fill();

            ctx.shadowBlur = 0;
            ctx.fillStyle = "#fff1b4";
            ctx.beginPath();
            ctx.arc(0, 0, c.r * .52, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        });
    }

    function drawParticles() {
        particles.forEach(p => {
            ctx.globalAlpha = Math.max(0, p.life / p.max);
            ctx.fillStyle = p.color;
            ctx.fillRect(p.x, p.y, 4, 4);
        });
        ctx.globalAlpha = 1;
    }

    function drawOverlayEffects() {
        // Vignette
        const vignette = ctx.createRadialGradient(
            W / 2, H / 2, 100, W / 2, H / 2, 760
        );
        vignette.addColorStop(0, "transparent");
        vignette.addColorStop(1, "#00000090");
        ctx.fillStyle = vignette;
        ctx.fillRect(0, 0, W, H);

        // Scan lines
        ctx.fillStyle = "#ffffff07";
        for (let y = 0; y < H; y += 5) {
            ctx.fillRect(0, y, W, 1);
        }

        if (!powerOn) {
            ctx.fillStyle = "#02040d20";
            ctx.fillRect(0, 0, W, H);
        }

        if (paused && !dead) {
            ctx.fillStyle = "#030815a8";
            ctx.fillRect(0, 0, W, H);
            ctx.fillStyle = "#eaf8ff";
            ctx.textAlign = "center";
            ctx.font = "bold 38px Courier New";
            ctx.fillText("PAUSED", W / 2, H / 2);
            ctx.font = "15px Courier New";
            ctx.fillText("PRESS P TO CONTINUE", W / 2, H / 2 + 32);
        }
    }

    function draw() {
        ctx.clearRect(0, 0, W, H);
        drawBackground();

        obstacles.forEach(o => {
            if (o.type === "bird") drawBird(o);
            else drawCactus(o);
        });

        drawCoins();
        drawDino();
        drawParticles();
        drawOverlayEffects();

        // Small in-game labels
        ctx.textAlign = "left";
        ctx.font = "12px Courier New";
        ctx.fillStyle = "#d7eaff";
        ctx.fillText("DISTANCE // " + Math.floor(score), 22, 30);

        ctx.textAlign = "right";
        ctx.fillStyle = powerOn ? "#8fffd0" : "#69caff";
        ctx.fillText(
            powerOn ? "SYSTEM NOMINAL" : "BATTERY CHARGE: " + battery,
            W - 22, 30
        );
    }

    function loop(timestamp) {
        const dt = Math.min((timestamp - lastTime) / 1000 || 0, .035);
        lastTime = timestamp;

        update(dt);
        draw();

        requestAnimationFrame(loop);
    }

    $("start").addEventListener("click", startGame);
    $("restart").addEventListener("click", startGame);

    $("pause").addEventListener("click", () => {
        if (!started || dead) return;
        paused = !paused;
        updateHUD();
    });

    $("powerButton").addEventListener("click", () => {
        powerOn = !powerOn;
        powerTimer = 0;
        burst(1000, 90, powerOn ? "#54ffc5" : "#55cfff", 20);
        beep(powerOn ? 750 : 220, .15);
        updateHUD();
    });

    window.addEventListener("keydown", event => {
        if (["Space", "ArrowUp", "ArrowDown"].includes(event.code)) {
            event.preventDefault();
        }

        if (event.repeat && event.code !== "ArrowDown") return;

        if (event.code === "Space" || event.code === "ArrowUp") {
            jump();
        } else if (event.code === "ArrowDown") {
            if (running && !paused) dino.ducking = true;
        } else if (event.code === "KeyP") {
            if (started && !dead) {
                paused = !paused;
                updateHUD();
            }
        } else if (event.code === "KeyR") {
            startGame();
        }
    });

    window.addEventListener("keyup", event => {
        if (event.code === "ArrowDown") {
            dino.ducking = false;
        }
    });

    canvas.addEventListener("pointerdown", event => {
        if (event.button !== 0) return;
        if (event.clientY > window.innerHeight * .7 &&
            event.pointerType === "touch") {
            jump();
        } else {
            jump();
        }
    });

    // Start screen is drawn immediately. Gameplay begins on START RUN.
    updateHUD();
    draw();
    requestAnimationFrame(loop);
})();
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(GAME)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
