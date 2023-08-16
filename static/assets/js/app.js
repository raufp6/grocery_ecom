const base_url = window.location.origin;
(function ($) {
    "use strict";
    // Category Edit View
    
    $(".button-add-to-cart").on('click',function(e){
        let $this = $(this);
        var product_has_variation = $('#product_has_variation').val()
        if(product_has_variation = ""){
            var product_has_variation = $this.data("hasvariation");
        }
        var product_id = $this.data("id");
        if($this.data("qty") == 1){
            var product_quantity = $this.data("qty");
        }else{
            var product_quantity = $('.product-qty-'+product_id).val();
        }
        var size = $('.package_size-'+product_id).val();
        if(product_has_variation == 1 && size == null){
            alerts('Please Select Package Size','error')
            return false
        }else{
            


            var data = {
                'quantity':product_quantity,
                'id':product_id,
                'package_size':size
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
        }
    });
    $(".button-increment-cart").on('click',function(e){
        let $this = $(this);
        var cart_id = $this.data("cartid");
        var data = {
            'quantity':1,
            'cart_id':cart_id,
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
        var cart_id = $this.data("cartid");
        // var product_quantity = $('.product-qty-'+product_id).val();
        
        console.log(cart_id);

        var data = {
            'quantity':1,
            'id':product_id,
            'cart_item_id':cart_id
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
                    location.reload()
                    
                }else{
                    alerts(resp.message,'error')
                }
            },error:function(resp){
                alerts("Error Occured",'error');
            }
        });
    });
    $(".button-delete-from-cart").on('click',function(e){
        let $this = $(this);
        var product_id = $this.data("id");
        var cart_id = $this.data("cartid");
        // var product_quantity = $('.product-qty-'+product_id).val();
        
        console.log(product_id);

        var data = {
            'id':product_id,
            'cart_id':cart_id
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
                    // $(".cart-items-count").html(resp.totalcartitems)
                    location.reload()
                    
                }else{
                    alerts(resp.message,'error')
                }
            },error:function(resp){
                alerts("Error Occured",'error');
            }
        });
    });
    $(".button-add-to-whishlist").on('click',function(e){
        let $this = $(this);
        var product_id = $this.data("id");
        
        var data = {
            'id':product_id,
        };
        $.ajax({
            url:$this.data("link"),
            type:'GET',
            data:data,
            dataType:'json',
            
            beforeSend:function(){
                console.log("Adding product to wishlist..");
            },
            success:function(resp){
                if(resp.status){
                    alerts(resp.message)
                    $(".wishlist-items-count").html(resp.whish_list_count)
                    
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
function expand_body_div(id)
{   
    $("option:selected").removeAttr("selected");
    $(".card-body").hide();
    $('#cancel_order_item_cancel_button_'+id).hide()
    $("#cancel_order_item_body_"+id).show();
}
function order_cancel_reason_change(val,item_id){
    if(val != ""){
        $('#cancel_order_item_cancel_button_'+item_id).show()   
    }else{
        $('#cancel_order_item_cancel_button_'+item_id).hide()   
    }
}
function get_vaarient_price(val){
    var current_price = parseInt($(".product-base-price").val());
    
    var data = {
        'id':val
    }
    $.ajax({
        url:"/get_variation_price/",
        type:'GET',
        data:data,
        dataType:'json',
        
        beforeSend:function(){
            console.log("Getting product variation price..");
        },
        success:function(resp){
            if(resp.status){
                console.log(resp.data)
                $(".product-selleing-price").val(resp.data.price)
                $(".current-price").html("₹"+resp.data.price)
                if(resp.data.mrp_price != 0){
                    $(".old-price").html("₹"+resp.data.mrp_price)
                }
                
                
                
            }else{
                alerts(resp.message,'error')
            }
        },error:function(resp){
            alerts("Error Occured",'error');
        }
    });
}