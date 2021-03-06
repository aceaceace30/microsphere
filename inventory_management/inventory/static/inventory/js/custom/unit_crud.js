jQuery(function($) {

  let loadForm = function () {
      let btn = $(this);

      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-unit").modal("show");
        },
        success: function (data) {
          $("#modal-unit .modal-content").html(data.html_form);
        }
      });
  };

  let saveForm = function () {
      let form = $(this);
      $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            $("#unit-data-table tbody").html(data.html_unit_list);
            $("#modal-unit").modal("hide");
          }
          else {
            $("#modal-unit .modal-content").html(data.html_form);
          }
        }
      });
      return false;
  };


// create unit
$(".js-create-unit").click(loadForm);
$("#modal-unit").on("submit", ".js-unit-create-form", saveForm);

// edit unit
$(".js-edit-unit").click(loadForm);
$("#modal-unit").on("submit", ".js-unit-edit-form", saveForm);

// delete unit
$("#unit-data-table").on("click", ".js-delete-unit", loadForm);
$("#modal-unit").on("submit", ".js-unit-delete-form", saveForm);



});