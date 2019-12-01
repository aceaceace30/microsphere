jQuery(function($) {

  let loadForm = function () {
      let btn = $(this);

      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-pm").modal("show");
        },
        success: function (data) {
          $("#modal-pm .modal-content").html(data.html_form);
        }
      });
  };

  let saveForm = function () {
      var form = $(this);

      $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            $("#modal-pm").modal("hide");

            // remove loader
            $("#loader").fadeOut("slow");

            // display notification message
            $("#notification_modal").modal("show");
            $("#notificationmodalLabel").html("PM has been created.");

            // refresh the page if modal is closed
            $("#notification_modal").on('hidden.bs.modal', function(){
                window.location.reload();
            });
            
            //$("#pm-data-table").DataTable().ajax.reload();
            //$("#pm-data-table tbody").html(data.html_pm_list);
          }
          else {
            $("#modal-pm .modal-content").html(data.html_form);
          }
        }
      });
      return false;
  };

// create unit
$(".js-create-pm").click(loadForm);
$("#modal-pm").on("submit", ".js-pm-create-form", saveForm);

// edit unit
// $(".js-edit-pm").click(loadForm);
// $("#modal-pm").on("submit", ".js-pm-edit-form", saveForm);

});