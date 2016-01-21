;
OL_FUNCS = {
  return_order: function($obj){
    $modal = $obj.closest('.modal');
    G_FUNCS.ajax_post($modal.find('form').find('input').first(), function(result){
      if(result.stat === 'success'){
        $modal.modal('hide');
      }
    });
  },

  return_shipping_checkbox: function($obj){
    if($obj.val() === "no_shipping"){
      $(".shipping_wrap").hide();
    }
    else{
      $(".shipping_wrap").show();
    }
  }
}
;

$(function(){
}).on('click', '.return_order', function(){
  OL_FUNCS.return_order($(this));
}).on('change', '.return_shipping_checkbox', function(){
  OL_FUNCS.return_shipping_checkbox($(this));
})
;
