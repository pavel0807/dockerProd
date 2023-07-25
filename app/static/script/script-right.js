const slider = document.querySelector(".slider-right");
const container = document.querySelector(".slider_container-right");
const slides = document.querySelectorAll(".slide-right");
//const navigations = document.querySelectorAll(".navigations");

let activeOrder = 0;


init();
function init() {
  for (let i =0;i<slides.length;i++){
    const slide = slides[i];

    slide.dataset.order = i;
    slide.style.transform = "translate(-50%, -50%);"
    slide.addEventListener('click',clickHandler);

  }
  activeOrder = Math.floor(slides.length / 2);



  update();
}

function update() {
  const  {width,height} = container.getBoundingClientRect();
  const  slideRect = slides[0].getBoundingClientRect();
  const a = width/4;
  const b = height/3;
  const delta = Math.PI / slides.length /2;

  for (let i =0;i<slides.length;i++){
    const upSlide = document.querySelector(
        `.slide-right[data-order="${activeOrder - i}"]`
    );

    if (upSlide) {
      upSlide.style.zIndex = slides.length - i;
      upSlide.style.filter = `blur(${Math.abs(i)}px)`;
      upSlide.style.left = `${
          width / 3 + a * Math.sin((Math.PI * 3)/2 - delta * i * 2) 
      }px`;
      upSlide.style.top = `${
          b  * Math.cos((Math.PI *3)/2 - delta * i * 2) + b
      }px`;
      upSlide.style.marginLeft =  `${
          20 * i
      }px`;
    }

    const downSlide = document.querySelector(
        `.slide-right[data-order="${activeOrder + i}"]`
    );
    if (downSlide) {
      downSlide.style.zIndex = slides.length - i;
      downSlide.style.filter = `blur(${Math.abs(i)}px)`;
      downSlide.style.left = `${
          width / 3 + a * Math.sin((Math.PI * 3)/2 + delta * i * 2)
      }px`;
      downSlide.style.top = `${
          b   * Math.cos((Math.PI *3)/2 + delta * i * 2) + b
      }px`;
      downSlide.style.marginLeft =  `${
          20 * i
      }px`;

    }
  }
}

function clickHandler()  {
  const order = parseInt(this.dataset.order,10);
  if (activeOrder == order) {
    let index = activeOrder+'-right';
    console.log(document.getElementById(index).innerHTML);
    document.location.href = document.location.href.replace("/main/",document.getElementById(index).innerHTML.substring(1));
  }
  else {
    activeOrder = order;
  }
  update();
}

