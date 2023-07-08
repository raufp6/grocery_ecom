const base_url = window.location.origin;
(function ($) {
    "use strict";
    // Category Edit View
    
    $(".button-add-to-cart").on('click',function(e){
        let $this = $(this);
        var product_id = $this.data("id");
        var product_quantity = $('.product-qty-'+product_id).val();
        var product_price = $this.data("sellingprice");
        var image = $this.data('image');
        var title = $this.data('title');
        console.log(product_id);
        console.log(product_quantity);
        console.log(product_price);
        console.log(image);
        console.log(title);


        var data = {
            'quantity':product_quantity,
            'id':product_id,
            'price':product_price,
            'image':image,
            'title':title
        };
        $.ajax({
            url:$this.data("link"),
            type:'GET',
            data:data,
            dataType:'json',
            
            beforeSend:function(){
                console.log("Adding product to cart..");
            },
            success:function(resp){
                if(resp.status){
                    alerts(resp.message)
                    // $this.html("Item added to cart")
                    $(".cart-items-count").html(resp.totalcartitems)
                    
                }else{
                    alerts(resp.message,'error')
                }
            },error:function(resp){
                alerts("Error Occured",'error');
            }
        });
    });
    $(".button-remove-to-cart").on('click',function(e){
        let $this = $(this);
        var product_id = $this.data("id");
        // var product_quantity = $('.product-qty-'+product_id).val();
        
        console.log(product_id);

        var data = {
            'quantity':1,
            'id':product_id,
        };
        $.ajax({
            url:$this.data("link"),
            type:'GET',
            data:data,
            dataType:'json',
            
            beforeSend:function(){
                console.log("Removing product from cart..");
            },
            success:function(resp){
                if(resp.status){
                    alerts(resp.message)
                    // $this.html("Item added to cart")
                    $(".cart-items-count").html(resp.totalcartitems)
                    
                }else{
                    alerts(resp.message,'error')
                }
            },error:function(resp){
                alerts("Error Occured",'error');
            }
        });
    });

 
       
})(jQuery);
function alerts(message,type='success'){
    if(type == 'success'){
        toastr.success(message)
    }else if(type == 'warning'){
        toastr.warning(message)
    }
    else if(type == 'error'){
        toastr.error(message)
    }
    
}