$("button.showhide").click(function() {

    if ($.trim($(this).text()) === 'Show Code') {
        $(this).text('Hide Code');
    } else {
        $(this).text('Show Code');
    }

});
//Hide Alert

$("#success-alert").hide();

//Span for Findings
arr = [];
var id;
$("#scn span").each(function(index, elem) {
    arr.push($(this).attr('id'));
});
for (i in arr) {
    id = arr[i] + "cp"
    var old;
    old = $("#" + arr[i]).text().split("-");
    old = old[0];
    id = get_findings_no(id);
    if (id === 0) {
        $("#" + arr[i]).parent().parent().parent().parent().hide();
    } else {
        $("#" + arr[i]).text(old + " - " + id);
    }

}
// Span for Invalid issues

arr1 = [];
var id1;
$("#scn1 span").each(function(index, elem) {
    arr1.push($(this).attr('id'));
});
for (i in arr1) {
    id1 = arr1[i] + "cp"
    var old1;
    old1 = $("#" + arr1[i]).text().split("-");
    old1 = old1[0];
    id1 = get_findings_no(id1);
    if (id1 === 0) {
        $("#" + arr1[i]).parent().parent().parent().parent().hide();
    } else {
        $("#" + arr1[i]).text(old1 + " - " + id1);
    }

}
//Get Findings no
function get_findings_no(id) {
    var id = "#" + id + " > div > div";
    return $(id).length
}
//Mark as resolved
function mark_resolved(scan_hash, finding_hash) {
    $.post("/resolve", {
            scan_hash: scan_hash,
            finding_hash: finding_hash
        },
        function(result) {
            $('#issue_modal').modal('hide');
            if (result.status === "ok") {
                setTimeout(function() {
                    $.bootstrapGrowl("Marked as Resolved!", {
                        type: 'success'
                    });
                }, 1000);
                setTimeout(function() {
                    location.reload();
                }, 2000);

            } else {
                setTimeout(function() {
                    $.bootstrapGrowl("Failed!", {
                        type: 'danger'
                    });
                }, 1000);
            }

        });
}
//Mark as resolved
function revert(scan_hash, finding_hash) {
    $.post("/revert", {
            scan_hash: scan_hash,
            finding_hash: finding_hash
        },
        function(result) {
            $('#revert_modal').modal('hide');
            if (result.status === "ok") {
                setTimeout(function() {
                    $.bootstrapGrowl("Moved into Issues", {
                        type: 'success'
                    });
                }, 1000);
                setTimeout(function() {
                    location.reload();
                }, 3000);

            } else {
                setTimeout(function() {
                    $.bootstrapGrowl("Failed!", {
                        type: 'danger'
                    });
                }, 1000);
            }

        });
}
//Mark as invalid
function mark_invalid(scan_hash, invalid_hash) {
    $.post("/invalid", {
            scan_hash: scan_hash,
            invalid_hash: invalid_hash
        },
        function(result) {
            $('#invalid_modal').modal('hide');
            if (result.status === "ok") {
                setTimeout(function() {
                    $.bootstrapGrowl("Marked as False Positive!", {
                        type: 'success'
                    });
                }, 1000);
                setTimeout(function() {
                    location.reload();
                }, 3000);
            } else {
                setTimeout(function() {
                    $.bootstrapGrowl("Failed!", {
                        type: 'danger'
                    });
                }, 1000);
            }

        });
}
//View file
function view(path, line, filename, scan_hash) {

    $.post('/view_file', {
            path: path,
            scan_hash: scan_hash
        },
        function(result) {
            $('#myModal').hide();
            $('#fname').text(filename.replace("<", "").replace(">", ""));
            $('#pth').text(path.replace("<", "").replace(">", ""));
            $("#bdy").html('<pre id="cnt"></pre>');
            $('#cnt').text(result.contents);
            $('#cnt').removeAttr('class');
            $('#cnt').attr('class', 'brush: js; highlight: ' + line);
            SyntaxHighlighter.defaults['quick-code'] = false;
            SyntaxHighlighter.highlight();
            $('#myModal').modal('show');

        });
}


$(document).keyup(function(e) {
    if (e.keyCode === 27) {
        $('#cls').click(); // esc
        $('#isu').click(); //not an issue close
        $('#inv').click(); // false positive close
        $('#bck').click(); // back to issues
    }
});