;
ACCOUNT_FUNCS = {

  charge_money: function($obj){
    $obj.hide();
    $("#charge_form").show();
  },

  cancel_charge: function($obj){
    $("#charge_form").hide();
    $("#charge_money").show();
  }

}
;

$(function(){
  G_FUNCS.countdown_each();
}).on('click', '.order_detail_toggle', function(){
  $('.order_detail').slideToggle();
}).on("click", "#charge_money", function(){
  ACCOUNT_FUNCS.charge_money($(this));
}).on("click", "#cancel_charge", function(){
  ACCOUNT_FUNCS.cancel_charge($(this));
})
;
