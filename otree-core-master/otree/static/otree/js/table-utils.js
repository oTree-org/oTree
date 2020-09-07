function createTableBodyFromJson(json)
{
    var html = '<tbody>', i, row, key, value;
    for (i in json) {
        row = json[i];
        html += '<tr>';
        for (key in row) {
            value = row[key];
            if (value === null) {
                value = '';
            }
            html += '<td data-field="' + key + '" title="' + value + '">' + value + '</td>';
        }
        html += '</tr>';
    }
    html += '</tbody>';
    return html;
}


function updateDraggable($table) {
    $table.toggleClass(
        'draggable',
        ($table.get(0).scrollWidth > $table.parent().width())
        || ($table.find('tbody').height() >= 450));
}

function updateTable($table, new_json) {
    var old_json = $table.data("raw");
    // build table for the first time
    if ( old_json === undefined ) {
        var tableBody = createTableBodyFromJson(new_json);
        $table.append(tableBody);
    }
    // compute delta and update
    // corresponding values in table
    else {
        var diffpatcher = jsondiffpatch.create({
            objectHash: function(obj) {
                return obj.participant_label;
            }
        });
        var delta = diffpatcher.diff(old_json, new_json);
        for (i in delta) {
            for (header_name in delta[i]) {

                var cell_to_update = $table.find(
                    "tbody tr:eq(" + i + ") td[data-field='" + header_name + "']" );
                var new_value = delta[i][header_name][1];
                cell_to_update.text(new_value);

                // so that we get tooltips if it truncates
                cell_to_update.prop('title', new_value);
                cell_to_update.css('background-color', 'green');
                cell_to_update.animate({
                        backgroundColor: "white"
                    },
                    5000
                );
            }
        }
    }
    $table.data("raw", new_json);
    updateDraggable($table);
}


function makeTableDraggable($table) {
    var mouseX, mouseY;
    $table.mousedown(function (e) {
        e.preventDefault();
        $table.addClass('grabbing');
        mouseX = e.pageX;
        mouseY = e.pageY;
    }).on('scroll', function () {
        $table.find('> thead, > tbody').width($table.width() + $table.scrollLeft());
    });
    $(document)
        .mousemove(function (e) {
            if (!$table.hasClass('grabbing')) {
                return;
            }
            e.preventDefault();
            $table.scrollLeft($table.scrollLeft() - (e.pageX - mouseX));
            var $tableBody = $table.find('tbody');
            $tableBody.scrollTop($tableBody.scrollTop() - (e.pageY - mouseY));
            mouseX = e.pageX;
            mouseY = e.pageY;
        }).mouseup(function (e) {
            if (!$table.hasClass('grabbing')) {
                return;
            }
            e.preventDefault();
            $table.removeClass('grabbing');
    });
}

function adjustCellWidths($table) {
    // Change the selector if needed
    $table = $($table);

    // Adjust the width of thead cells when window resizes
    $(window).resize(function() {
        // Get the tbody columns width array
        var $bodyCells = $table.find('tbody tr:first').children();
        var colWidths = $bodyCells.map(function() {
            return $(this).width();
        }).get();

        // Set the width of thead columns
        $table.find('thead tr:last').children().each(function(i, v) {
            $(v).width(colWidths[i]);
        });
    }).resize(); // Trigger resize handler    
}
