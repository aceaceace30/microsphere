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

  $("#id_area").filter(function() {
      var url = $("#create-inventory").attr("data-url");  // get the url of the `load_business_units` view
      var area = $(this).val();                           // get the selected area from the HTML input
      var business_unit = $("#id_business_unit").val();

      $.ajax({                                            // initialize an AJAX request
        url: url,                                         // set the url of the request
        data: {
          'area': area,                                   // add the area to the GET parameters
          'business_unit': business_unit,
        },
        success: function (data) {                        // `data` is the return of the `load_business_units` view function
          $("#id_business_unit").html(data);              // replace the contents of the business_unit input with the data that came from the server
        }
      });
  });

  $("#id_area").change(function () {
      var url = $("#create-inventory").attr("data-url");  // get the url of the `load_business_units` view
      var area = $(this).val();                           // get the selected area from the HTML input

      $.ajax({                                            // initialize an AJAX request
        url: url,                                         // set the url of the request
        data: {
          'area': area                                    // add the area to the GET parameters
        },
        success: function (data) {                        // `data` is the return of the `load_business_units` view function
          $("#id_business_unit").html(data);              // replace the contents of the business_unit input with the data that came from the server
        }
      });
  });

  // $("#id_machine_brand").filter(function () {
  //     var url = $("#create-inventory").attr("data-model-url");  // get the url of the `load_business_units` view
  //     var machine_type = $('#id_machine_type').val();
  //     var machine_brand = $(this).val();                           // get the selected area from the HTML input
  //     //var model = $('#id_model').val();

  //     $.ajax({                                            // initialize an AJAX request
  //       url: url,                                         // set the url of the request
  //       data: {
  //         'machine_type':machine_type,                                    // add the area to the GET parameters
  //         'machine_brand':machine_brand,
  //         //'model':model,
  //       },
  //       success: function (data) {                        // `data` is the return of the `load_business_units` view function
  //         $("#id_model").html(data);              // replace the contents of the business_unit input with the data that came from the server
  //       }
  //     });
  // });

  $("#id_machine_brand").change(function () {
      var url = $("#create-inventory").attr("data-model-url");  // get the url of the `load_business_units` view
      var machine_type = $('#id_machine_type').val();
      var machine_brand = $(this).val();                           // get the selected area from the HTML input

      $.ajax({                                            // initialize an AJAX request
        url: url,                                         // set the url of the request
        data: {
          'machine_type': machine_type,                                    // add the area to the GET parameters
          'machine_brand':machine_brand,
        },
        success: function (data) {
          $("#id_model").html(data);              // replace the contents of the business_unit input with the data that came from the server
        }
      });
  });

  // $("#id_machine_type").change(function () {
  //     var url = $("#create-inventory").attr("data-model-url");  // get the url of the `load_business_units` view
  //     var machine_type = $(this).val();
  //     var machine_brand = $('#id_machine_brand').val();                           // get the selected area from the HTML input

  //     $.ajax({                                            // initialize an AJAX request
  //       url: url,                                         // set the url of the request
  //       data: {
  //         'machine_type': machine_type,                                    // add the area to the GET parameters
  //         'machine_brand':machine_brand,
  //       },
  //       success: function (data) {
  //         $("#id_model").html(data);              // replace the contents of the business_unit input with the data that came from the server
  //       }
  //     });
  // });


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