/*
Lame trick...I increment the filename when I release a new version of this file,
because on runserver, Chrome caches it, so all oTree users developing on Chrome
would need to Ctrl+F5.
 */

function populateTableBody($tbody, rows)
{
    var html = '';
    for (var i in rows) {
        html += createTableRow(rows[i]);
    }
    $tbody.append(html);
}

function createTableRow(row)
{
   var html = '<tr>';
    for (var key in row) {
        var value = row[key];
        if (value === null) {
            value = '';
        }
        html += '<td data-field="' + key + '" title="' + value + '">' + value + '</td>';
    }
    html += '</tr>';
    return html;
}

function updateDraggable($table) {
    $table.toggleClass(
        'draggable',
        ($table.get(0).scrollWidth > $table.parent().width())
        || ($table.find('tbody').height() >= 450));
}

function flashGreen($ele) {
    $ele.css('background-color', 'green');
    $ele.animate({
            backgroundColor: "white"
        },
        5000
    );
}

function updateTable($table, new_json) {
    var old_json = $table.data("raw");
    var $tbody = $table.find('tbody');
    // build table for the first time
    if ( old_json === undefined ) {
        populateTableBody($tbody, new_json);
    }
    // compute delta and update
    // corresponding values in table
    else {
        var diffpatcher = jsondiffpatch.create({
            objectHash: function(obj) {
                // it's not actually participant.label, it's
                // participant._id_in_session e.g. P1, P2... not sure why
                // it was called that
                return obj.participant_label;
            }
        });
        var delta = diffpatcher.diff(old_json, new_json);
        for (i in delta) {
            // 2017-08-13: when i have time, i should update this
            // to the refactor I did in SessionMonitor.html
            for (header_name in delta[i]) {

                var cell_to_update = $table.find(
                    "tbody tr:eq(" + i + ") td[data-field='" + header_name + "']" );
                var new_value = delta[i][header_name][1];
                cell_to_update.text(new_value);

                // so that we get tooltips if it truncates
                cell_to_update.prop('title', new_value);
                flashGreen(cell_to_update);
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
