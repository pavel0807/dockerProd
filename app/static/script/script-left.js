const sliderLeft = document.querySelector(".slider-left");
const containerLeft = document.querySelector(".slider_container-left");
const slidesLeft = document.querySelectorAll(".slide-left");
//const navigations = document.querySelectorAll(".navigations");

let activeOrderLeft = 0;


initLeft();
function initLeft() {
  for (let i =0;i<slidesLeft.length;i++){
    const slideLeft = slidesLeft[i];

    slideLeft.dataset.order = i;
    slideLeft.style.transform = "translate(-50%, -50%);"
    slideLeft.addEventListener('click',clickHandlerLeft)
  }
  activeOrderLeft = Math.floor(slidesLeft.length / 2);

  updateLeft();
}

function updateLeft() {
  const  {width,height} = containerLeft.getBoundingClientRect();
  const  slideRectLeft = slidesLeft[0].getBoundingClientRect();
  const aLeft = width/4;
  const bLeft = height/3;
  const deltaLeft = Math.PI / slidesLeft.length /2;

  for (let i =0;i<slidesLeft.length;i++){
    const upSlideLeft = document.querySelector(
        `.slide-left[data-order="${activeOrderLeft - i}"]`
    );

    if (upSlideLeft) {
      upSlideLeft.style.zIndex = slidesLeft.length - i;
      //upSlideLeft.style.blur = (`${Math.abs(20 * i)}px`);
      upSlideLeft.style.filter = `blur(${Math.abs(i)}px)`;
      //upSlideLeft.querySelector("img").style.blur = "1.5rem";
      //upSlideLeft.style.opacity = 1 - (2 * i) / slidesLeft.length;
      upSlideLeft.style.left = `${
          width / 3 + aLeft * Math.sin(-(Math.PI * 3)/2 - deltaLeft * i * 2)
      }px`;
      upSlideLeft.style.top = `${
          bLeft  * Math.cos((Math.PI *3)/2 - deltaLeft * i * 2) + bLeft
      }px`;
      upSlideLeft.style.marginLeft =  `${
          - 20 * i
      }px`;
    }

    const downSlideLeft = document.querySelector(
        `.slide-left[data-order="${activeOrderLeft + i}"]`
    );
    if (downSlideLeft) {
      downSlideLeft.style.zIndex = slidesLeft.length - i;
      //downSlideLeft.style.opacity = 1 - (2 * i) / slidesLeft.length;
      downSlideLeft.style.filter = `blur(${Math.abs(i)}px)`;
      downSlideLeft.style.left = `${
          width / 3 + aLeft * Math.sin(-(Math.PI * 3)/2 + deltaLeft * i * 2) 
      }px`;
      downSlideLeft.style.top = `${
          bLeft   * Math.cos((Math.PI *3)/2 + deltaLeft * i * 2) + bLeft
      }px`;
      downSlideLeft.style.marginLeft =  `${
          - 20 * i
      }px`;

    }
  }
}

function clickHandlerLeft()  {
  const orderLeft = parseInt(this.dataset.order,10);
  if (activeOrderLeft == orderLeft) {
    var MyDiv1 = document.getElementById(activeOrderLeft+'-left');
    console.log(MyDiv1.innerHTML.substring(1));
    window.location.href = document.location.href.replace(document.location.pathname,MyDiv1.innerHTML.substring(1));
  }
  else {
    activeOrderLeft = orderLeft;
  }
  updateLeft();
}

