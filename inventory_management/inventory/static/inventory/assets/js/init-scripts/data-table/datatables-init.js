(function ($) {
    //    "use strict";


    /*  Data Table
    -------------*/

    $('#unit-data-table thead th').each( function () {
        var title = $(this).text();
        if (title != 'Action') {
            $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
        }
    } );

    // $('#bootstrap-data-table').DataTable({
    //     lengthMenu: [[10, 20, 50, -1], [10, 20, 50, "All"]],
    // });

    var unit_table = $('#unit-data-table').DataTable({
        lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
        //buttons: ['copy', 'csv', 'excel', 'pdf', 'print'],
    });

    unit_table.columns().every( function () {
        var that = this;
 
        $( 'input', this.header() ).on( 'keyup change clear', function () {
            if ( that.search() !== this.value ) {
                that
                    .search( this.value )
                    .draw();
            }
        });
    });

    $('#pm-data-table thead th').each( function () {
        var title = $(this).text();
        if (title != 'Status') {
            $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
        }
    } );

    $('#bootstrap-data-table').DataTable({
        lengthMenu: [[10, 20, 50, -1], [10, 20, 50, "All"]],
    });

    var pm_table = $('#pm-data-table').DataTable({
        lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
        buttons: ['copy', 'csv', 'excel', 'pdf', 'print'],
    });

    pm_table.columns().every( function () {
        var that = this;
 
        $( 'input', this.header() ).on( 'keyup change clear', function () {
            if ( that.search() !== this.value ) {
                that
                    .search( this.value )
                    .draw();
            }
        });
    });

	$('#row-select').DataTable( {
        initComplete: function () {
				this.api().columns().every( function () {
					var column = this;
					var select = $('<select class="form-control"><option value=""></option></select>')
						.appendTo( $(column.footer()).empty() )
						.on( 'change', function () {
							var val = $.fn.dataTable.util.escapeRegex(
								$(this).val()
							);

							column
								.search( val ? '^'+val+'$' : '', true, false )
								.draw();
						} );

					column.data().unique().sort().each( function ( d, j ) {
						select.append( '<option value="'+d+'">'+d+'</option>' )
					} );
				} );
			}
		} );

})(jQuery);
