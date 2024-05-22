const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.btnLogin');
const iconClose = document.querySelector('.icon-close');
const wrapperMain = document.querySelector('.wrapperMain');
const popup = document.querySelector('.popup');
const iconTheme = document.querySelector('.theme');
const popupReview = document.querySelector('.popup-review');
const popupReviewBtn = document.querySelector('.reviewBtn');
const popupReviewBtnClose = document.querySelector('.reviewPopupClose');
let list = document.querySelectorAll('.list li');
let cards = document.querySelectorAll('.card');





// Модальное окно авторизации и регистрации
registerLink.addEventListener('click', ()=> {
    wrapper.classList.add('active');
})

loginLink.addEventListener('click', ()=>{
    wrapper.classList.remove('active');
})

btnPopup.addEventListener('click', ()=>{
    wrapper.classList.add('active-popup');
    wrapperMain.classList.add('lock');
    popup.classList.add('active');
    console.log('OK')
})

iconClose.addEventListener('click', ()=>{
    wrapper.classList.remove('active-popup');
    wrapperMain.classList.remove('lock');
})


// Темная тема
function darkmode(){
    const wasDarkmode = localStorage.getItem('darkmode') == 'true'
    localStorage.setItem('darkmode', !wasDarkmode)
    wrapperMain.classList.toggle('dark-mode', !wasDarkmode)
  }
  
iconTheme.addEventListener('click', darkmode)
  
function onload() {
    wrapperMain.classList.toggle('dark-mode',localStorage.getItem('darkmode') == 'true')
}
  
document.addEventListener('DOMContentLoaded', onload);


// Фильтр каталога
list.forEach((el) => {
    el.addEventListener("click", (e)=>{
        list.forEach((li)=>{
            li.classList.remove("active");
        })
        e.target.classList.add("active");

        cards.forEach((el2)=>{
            el2.style.display = "none";
        })
        document.querySelectorAll(e.target.dataset.filter).forEach((li)=>{
            li.style.display = "flex";
        })
    })
})


// Слайдер
var swiper = new Swiper(".slide-content", {
    slidesPerView: 3,
    mousewhell: true,
    keyboard: true,
    spaceBetween: 30,
    loop: true,
    centerSlide: 'true',
    fade: 'true',
    grabCursor: 'true',
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
      dynamicBullets: true,
    },
    breakpoints:{
        0: {
            slidesPerView: 1,
        },
        520: {
            slidesPerView: 2,
        },
        950: {
            slidesPerView: 3,
        }
    }
});


// Модальное окно для отзыва
popupReviewBtn.addEventListener('click', ()=> {
    popupReview.classList.add('open-popup');
})

popupReviewBtnClose.addEventListener('click', ()=>{
    popupReview.classList.remove('open-popup');
})