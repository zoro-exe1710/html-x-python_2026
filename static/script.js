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
    const result = document.getElementById("result");
    result.innerHTML = "";

    // 🔥 SHOW MAIN HEADING AFTER NAME IS ENTERED
    const heading = document.getElementById("main-heading");
    heading.style.display = "block";

    document.getElementById("panda-container").style.display = "none";

    const fullText = `${data}`;
    typeWriter(result, fullText, 0);
});

    document.getElementById("music").play();
}

// Typing effect function
function typeWriter(element, text, i) {
    if (i < text.length) {
        element.innerHTML += text.charAt(i) === "\n" ? "<br>" : text.charAt(i);
        i++;
        setTimeout(() => typeWriter(element, text, i), 85); // 40ms per character
    }
}

/* FIREWORKS CODE BELOW */
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

const colors = ["red", "yellow", "orange", "lime", "cyan", "magenta", "white", "gold"];

class Rocket {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = canvas.height;
        this.speed = Math.random() * 1.5 + 2.5;
        this.angle = Math.random() * Math.PI / 4 - Math.PI / 8;
        this.color = colors[Math.floor(Math.random() * colors.length)];
        this.exploded = false;
    }

    update() {
        this.y -= this.speed * Math.cos(this.angle);
        this.x += this.speed * Math.sin(this.angle);
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
        this.radius = Math.random() * 2 + 1;
        const speed = Math.random() * 4 + 2;
        const angle = Math.random() * 2 * Math.PI;
        this.speedX = Math.cos(angle) * speed;
        this.speedY = Math.sin(angle) * speed;
        this.life = 120;
    }

    update() {
        this.x += this.speedX;
        this.y += this.speedY;
        this.speedY += 0.05;
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

    if (Math.random() < 0.03) {
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
