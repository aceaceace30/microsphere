jQuery(function($) {
  // $(document).ready(function(){

  // };

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

  $("#id_machine_brand").filter(function () {
      var url = $("#create-inventory").attr("data-model-url");  // get the url of the `load_business_units` view
      var machine_type = $('#id_machine_type').val();
      var machine_brand = $(this).val();                           // get the selected area from the HTML input
      var model = $('#id_model').val();

      $.ajax({                                            // initialize an AJAX request
        url: url,                                         // set the url of the request
        data: {
          'machine_type':machine_type,                                    // add the area to the GET parameters
          'machine_brand':machine_brand,
          'model':model,
        },
        success: function (data) {                        // `data` is the return of the `load_business_units` view function
          $("#id_model").html(data);              // replace the contents of the business_unit input with the data that came from the server
        }
      });
  });

  $("#id_machine_brand").change(function () {
      var url = $("#create-inventory").attr("data-model-url");  // get the url of the `load_business_units` view
      var machine_type = $('#id_machine_type').val();
      var machine_brand = $(this).val();

      alert(url);
      alert(machine_type);
      alert(machine_brand);                           // get the selected area from the HTML input

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

});