$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus_cart').click(function (){
  var id = $(this).attr('pid').toString();
  var quan = this.parentNode.children[2];
  var amount = document.getElementById('amount');
  var totalamount = document.getElementById('totalamount');
  $.ajax({
    type:'get',
    url:'addcartplus',
    data:{
      prod_id:id
    },
    success: function(data){
      quan.innerText = data.quantity
      amount.innerText = data.totalamount
      totalamount.innerText = data.finalamount
    }
  });
});

$('.minus_cart').click(function (){
  let id = $(this).attr('pid').toString();
  let quan = this.parentNode.children[2];
  var amount = document.getElementById('amount');
  var totalamount = document.getElementById('totalamount');
  $.ajax({
    type:'get',
    url:'addcartminus',
    data:{
      prod_id: id
    },
    success: function(data){
      quan.innerText = data.quantity
      amount.innerText = Math.abs(data.totalamount)
      totalamount.innerText = Math.abs(data.finalamount)
    }
  });
});