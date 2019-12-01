jQuery(function($) {
// auto load the choices for edit view in business unit
  $("#id_area").filter(function() {

      var url = $("#create-inventory").attr("data-url");  // get the url of the `load_business_units` view
      var area = $(this).val();                           // get the selected area from the HTML input
      var business_unit = $("#id_business_unit").val();
      var client = $('#id_client').val();

      $.ajax({                                            // initialize an AJAX request
        url: url,                                         // set the url of the request
        data: {
          'area': area,                                   // add the area to the GET parameters
          'business_unit': business_unit,
          'client': client,
        },
        success: function (data) {                        // `data` is the return of the `load_business_units` view function
          $("#id_business_unit").html(data);              // replace the contents of the business_unit input with the data that came from the server
        }
      });
  });

// change the value of business unit based on area value
  $("#id_area").change(function () {
      var url = $("#create-inventory").attr("data-url");  // get the url of the `load_business_units` view
      var area = $(this).val();                           // get the selected area from the HTML input
      var client = $('#id_client').val();

      $.ajax({                                            // initialize an AJAX request
        url: url,                                         // set the url of the request
        data: {
          'area': area,                                    // add the area to the GET parameters
          'client': client,
        },
        success: function (data) {                        // `data` is the return of the `load_business_units` view function
          $("#id_business_unit").html(data);              // replace the contents of the business_unit input with the data that came from the server
        }
      });
  });

// auto load the choices
  $("#id_client").filter(function () {
      var url = $("#create-inventory").attr("data-url");
      var client = $(this).val();
      var area = $('#id_area').val();

      $.ajax({
        url: url,
        data: {
          'client': client,
          'area': area,
        },
        success: function (data) {
          $("#id_business_unit").html(data);
        }
      });
  });

  $("#id_client").change(function () {
      var url = $("#create-inventory").attr("data-url");
      var client = $(this).val();
      var area = $('#id_area').val();

      $.ajax({
        url: url,
        data: {
          'client': client,
          'area': area,
        },
        success: function (data) {
          $("#id_business_unit").html(data);
        }
      });
  });

// auto load the choices
  $("#id_machine_type").filter(function () {
      var url = $("#create-inventory").attr("data-brand-url");
      var machine_type = $(this).val();
      var machine_brand = $('#id_machine_brand').val();

      $.ajax({
        url: url,
        data: {
          'machine_type': machine_type,
          'machine_brand': machine_brand,
        },
        success: function (data) {
          $("#id_machine_brand").html(data);
        }
      });
  });

// change the value based from selection
  $("#id_machine_type").change(function () {

      // reset the value of model dropdown if machine type is changed
      $("#id_model option[value!='']").each(function() {
          $(this).remove();
      });

      var url = $("#create-inventory").attr("data-brand-url");
      var machine_type = $(this).val();

      $.ajax({
        url: url,
        data: {
          'machine_type': machine_type,
        },
        success: function (data) {
          $("#id_machine_brand").html(data);
        }
      });
  });

  $("#id_machine_brand").filter(function () {
      var url = $("#create-inventory").attr("data-model-url");
      var machine_type = $('#id_machine_type').val();
      var machine_brand = $(this).val();
      var model = $('#id_model').val();

      $.ajax({
        url: url,
        data: {
          'machine_type': machine_type,
          'machine_brand': machine_brand,
          'model': model,
        },
        success: function (data) {
          $("#id_model").html(data);
        }
      });
  });

  $("#id_machine_brand").change(function () {
      var url = $("#create-inventory").attr("data-model-url");
      var machine_type = $('#id_machine_type').val();
      var machine_brand = $(this).val();

      $.ajax({
        url: url,
        data: {
          'machine_type': machine_type,
          'machine_brand':machine_brand,
        },
        success: function (data) {
          $("#id_model").html(data);
        }
      });
  });

});