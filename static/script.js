function getWish() {
    let name = document.getElementById("name").value.trim();

    if (name === "") {
        document.getElementById("result").innerHTML =
            "⚠️ Please enter your name to unlock the New Year surprise 🎁";
        return;
    }

    fetch("/wish", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name: name })
    })
    .then(res => res.text())
    .then(data => {
        document.getElementById("result").innerHTML =
            `🎉 Happy New Year 2025, ${name}! 🎊<br>${data}`;
    });

    document.getElementById("music").play();
}
const canvas = document.getElementById("fireworks");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

window.onresize = () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
};

let rockets = [];
let particles = [];

const colors = [
    "red", "yellow", "orange", "lime",
    "cyan", "magenta", "white", "gold"
];

class Rocket {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = canvas.height;
        this.speed = Math.random() * 3 + 5;
        this.color = colors[Math.floor(Math.random() * colors.length)];
        this.exploded = false;
    }

    update() {
        this.y -= this.speed;
        if (this.y < canvas.height / 3) {
            this.exploded = true;
            explode(this.x, this.y, this.color);
        }
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, 3, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
    }
}

class Particle {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.radius = Math.random() * 3 + 1;
        this.speedX = (Math.random() - 0.5) * 8;
        this.speedY = (Math.random() - 0.5) * 8;
        this.life = 100;
    }

    update() {
        this.x += this.speedX;
        this.y += this.speedY;
        this.life--;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
    }
}

function explode(x, y, color) {
    for (let i = 0; i < 80; i++) {
        particles.push(new Particle(x, y, color));
    }
}

function animateFireworks() {
    ctx.fillStyle = "rgba(0,0,0,0.2)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (Math.random() < 0.05) {
        rockets.push(new Rocket());
    }

    rockets.forEach((r, i) => {
        r.update();
        r.draw();
        if (r.exploded) rockets.splice(i, 1);
    });

    particles.forEach((p, i) => {
        p.update();
        p.draw();
        if (p.life <= 0) particles.splice(i, 1);
    });

    requestAnimationFrame(animateFireworks);
}

animateFireworks();
