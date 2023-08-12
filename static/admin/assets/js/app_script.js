const base_url = window.location.origin;
(function ($) {
    "use strict";
    // Category Edit View
    $("#table tbody").on("click",".link-edit-category",function(e){
        e.preventDefault();
        var $this = $(this);
        let cid = $this.parents(".record").find('td').eq(1).text();
        let title = $this.parents(".record").find('td').eq(2).text();
        let image = $this.data('img')
        let is_featured = $this.data('featured')
        let is_available = $this.data('available')
        let url = $this.attr('href');

        
        $('#FormCategoryEdit').attr("action",url);
        $('#FormCategoryEdit input[name="title"]').val(title);
        $('#FormCategoryEdit input[name="old_title"]').val(title);
        $('#current_image').attr("src",image);
        if(is_featured == true){
            $('#is_featured').prop('checked',true);
        }
        $('#is_available option[value='+is_available+']').attr('selected','selected');
        $('#category_edit').modal('show');
        return false;
    });

    //Category Update
    $("#FormCategoryEdit").on('submit',function(e){
        e.preventDefault();
        e.stopPropagation();
        let $this = $(this);
        var data = new FormData(this);

        $.ajax({
            url:$('#FormCategoryEdit').attr("action"),
            type:'POST',
            data:data,
            dataType:'json',
            mimeType: "multipart/form-data",
            processData: false,
            contentType: false,
            success:function(resp){
                if(resp.message == "success"){
                    alerts(resp.message)
                    location.reload(); 
                    
                }else{
                    alerts(resp.message,'error')
                }
            },error:function(resp){
                alert(resp.message);
            }
        });

        return false
    });
    $(".button-add-to-cart").click(function(e){
        alert("sd");
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