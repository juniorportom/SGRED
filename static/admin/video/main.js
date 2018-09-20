var formAjaxSubmit = function (form, modal) {
    $(form).submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function (xhr, ajaxOptions, thrownError) {
                if ($(xhr).find('.has-error').length > 0) {
                    $(modal).find('.modal-body').html(xhr);
                    formAjaxSubmit(form, modal);
                } else {
                   $(modal).modal('toggle');
                  // myAlertTop();
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
            }
        });
    });
}


$(function () {
    $("#idSelTipo").selectmenu({
        change: function (event, data) {
            this.form.submit();
        }
    });

    $("#idSelCategorias").selectmenu({
        change: function (event, data) {
            this.form.submit();
        }
    });


});

function myAlertTop(){
  $(".myAlert-top").show();
  setTimeout(function(){
    $(".myAlert-top").hide();
  }, 2000);
}

function myAlertBottom(){
  $(".myAlert-bottom").show();
  setTimeout(function(){
    $(".myAlert-bottom").hide();
  }, 2000);
}


