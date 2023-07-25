function fun1() {
    var rng=document.getElementById('count_donat'); //rng - это ползунок
    var i1=document.getElementById('enter_count_donat'); // i1 - input
    i1.value=rng.value;
}

var r = $('count_donat').slider()
    .data('slider');