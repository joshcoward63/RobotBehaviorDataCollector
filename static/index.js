const splash = document.querySelector('.splash');
const start = document.getElementById("start");
const startBot = document.querySelector('.startBot');
const startBotButton = document.getElementById("startBotButton")

start.onclick = function(){
       setTimeout(()=>{
        splash.classList.add('display-none');
}, 2000); 
console.log("js is working and so is python")
}

startBotButton.onclick = function(){
        setTimeout(()=>{
         startBot.classList.add('display-none');
 }, 2000); 
 console.log("startBotButton has been clicked!");
 }

 
const header = document.querySelector(".header");

window.onscroll = function(){
        var top = window.scrollY;
        console.log(top);
        if(top>=50){
                header.classList.add('active');
        }
        else{
                header.classList.remove("active");
        }
}

// const startBot = document.getElementById("startBot");

// startBot.onclick = function(){
//         $.ajax({
//                 type: "POST",
//                 url: "/randomBehavior.py",
//                 data: { param: text}
//               }).done(function( o ) {
//                  // do something
//               });
// }