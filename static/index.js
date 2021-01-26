/*The Following are the buttons used in the html page*/
const splash = document.querySelector('.splash');
const start = document.getElementById("start");
const startBot = document.querySelector('.startBot');
const startBotButton = document.getElementById("startBotButton")
const submitButton = document.getElementById("submitButton");
/*The Following are the user description and */
const descriptionField = document.getElementById("description");
const interest_alarm = document.getElementsByName("likert2");
const confusion_understanding = document.getElementsByName("likert3");
const frusteration_relief = document.getElementsByName("likert4");
const sorrow_joy = document.getElementsByName("likert5");
const anger_gratitude = document.getElementsByName("likert6");
const fear_hope = document.getElementsByName("likert7");
const boredom_surprise = document.getElementsByName("likert8");
const disgust_desire = document.getElementsByName("likert9");

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

submitButton.onclick = function(){

}
 



// const header = document.querySelector(".header");

// window.onscroll = function(){
//         var top = window.scrollY;
//         console.log(top);
//         if(top>=50){
//                 header.classList.add('active');
//         }
//         else{
//                 header.classList.remove("active");
//         }
// }