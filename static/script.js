function getWish(){
    let name=document.getElementById("name").value.trim();
    if(name===""){
        document.getElementById("result").innerHTML="⚠️ Please enter your name to unlock the New Year surprise 🎁";
        return;
    }

    fetch("/wish",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({name:name})
    })
    .then(res=>res.text())
    .then(quote => {
    const result = document.getElementById("result");
    result.innerHTML = "";

    document.getElementById("main-heading").style.display = "block";

    const fullText = `<strong>Dear ${name},</strong>\n\n${quote}`;
    typeWriter(result, fullText, 0);
});


    document.getElementById("music").play();
}

function typeWriter(element, text, i) {
    if (i < text.length) {
        element.innerHTML += text.charAt(i) === "\n" ? "<br>" : text.charAt(i);
        setTimeout(() => typeWriter(element, text, i + 1), 40);
    }
}


const canvas=document.getElementById("fireworks"),ctx=canvas.getContext("2d");
canvas.width=window.innerWidth;
canvas.height=window.innerHeight;

window.onresize=()=>{
    canvas.width=window.innerWidth;
    canvas.height=window.innerHeight;
};

let rockets=[],particles=[];
const colors=["red","yellow","orange","lime","cyan","magenta","white","gold"];

class Rocket{
    constructor(){
        this.x=Math.random()*canvas.width;
        this.y=canvas.height;
        this.speed=Math.random()*1.2+1.5;
        this.color=colors[Math.floor(Math.random()*colors.length)];
        this.exploded=false;
    }
    update(){
        this.y-=this.speed;
        if(this.y<canvas.height/3){
            this.exploded=true;
            explode(this.x,this.y,this.color);
        }
    }
    draw(){
        ctx.beginPath();
        ctx.arc(this.x,this.y,3,0,Math.PI*2);
        ctx.fillStyle=this.color;
        ctx.fill();
    }
}

class Particle{
    constructor(x,y,c){
        this.x=x;
        this.y=y;
        this.color=c;
        this.radius=Math.random()*2+1;
        const s=Math.random()*3+1;
        const a=Math.random()*Math.PI*2;
        this.vx=Math.cos(a)*s;
        this.vy=Math.sin(a)*s;
        this.life=140;
    }
    update(){
        this.x+=this.vx;
        this.y+=this.vy;
        this.vy+=0.03;
        this.life--;
    }
    draw(){
        ctx.beginPath();
        ctx.arc(this.x,this.y,this.radius,0,Math.PI*2);
        ctx.fillStyle=this.color;
        ctx.fill();
    }
}

function explode(x,y,c){
    for(let i=0;i<60;i++)particles.push(new Particle(x,y,c));
}

function animate(){
    ctx.fillStyle="rgba(0,0,0,0.25)";
    ctx.fillRect(0,0,canvas.width,canvas.height);

    if(Math.random()<0.015)rockets.push(new Rocket());

    rockets.forEach((r,i)=>{
        r.update();
        r.draw();
        if(r.exploded)rockets.splice(i,1);
    });

    particles.forEach((p,i)=>{
        p.update();
        p.draw();
        if(p.life<=0)particles.splice(i,1);
    });

    requestAnimationFrame(animate);
}

animate();


