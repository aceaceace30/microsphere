$(document).ready(function () {

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
            $("#pm-table tbody").html(data.html_pm_list);
            $("#modal-pm").modal("hide");
          }
          else {
            $("#modal-pm .modal-content").html(data.html_form);
          }
        }
      });
      return false;
  };

  let tagForm = function () {
      var form = $(this);
      $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            $("#pm-table tbody").html(data.html_pm_list);
            $("#modal-tag-pm").modal("hide");
          }
          else {
            $("#modal-tag-pm .modal-content").html(data.html_form);
          }
        }
      });
      return false;
  };

// create unit
$(".js-create-pm").click(loadForm);
$("#modal-pm").on("submit", ".js-pm-create-form", saveForm);

// edit unit
$(".js-edit-pm").click(loadForm);
$("#modal-pm").on("submit", ".js-pm-edit-form", saveForm);

// delete unit
$("#pm-table").on("click", ".js-delete-pm", loadForm);
$("#modal-pm").on("submit", ".js-pm-delete-form", saveForm);

// mark done pm
$("#pm-table").on("click", ".js-tag-pm", loadForm);
$("#modal-tag-pm").on("submit", ".js-pm-tag-form", tagForm);

});