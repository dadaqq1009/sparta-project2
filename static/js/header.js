$(function(){

  var box = 0;
  $(".status").click(function(){
    if(box == 0){
      $(".status_box").show();
      $(".status_box").animate({height:200});
      box = 1;
    } else{
      $(".status_box").hide();
      $(".status_box").animate({height:0});
      box = 0;
    }
  });
});