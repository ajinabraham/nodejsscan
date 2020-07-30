$(document).ready(function () {
   


//View file
window.view = function(path, line, filename, scan_hash) {
    $.post('/view_file', {
        path: path,
        scan_hash: scan_hash
    },
        function (result) {
            var toarr = JSON.parse(line);
            var expanded = [];
            var i;
            for (i = toarr[0]; i <= toarr[1]; i++) {
                expanded.push(i);
            }
            $('#myModal').hide();
            $('#fname').text(filename.replace(/</g, "").replace(/>/g, ""));
            $('#pth').text(path.replace(/</g, "").replace(/>/g, ""));
            $("#bdy").html('<pre id="cnt"></pre>');
            $('#cnt').text(result.contents);
            $('#cnt').removeAttr('class');
            $('#cnt').attr('class', 'brush: js; highlight: ' + JSON.stringify(expanded));
            SyntaxHighlighter.defaults['quick-code'] = false;
            SyntaxHighlighter.highlight();
            
            
            $('#myModal').modal('show');
            const hcls = document.getElementsByClassName("highlighted")[0];
            if (hcls) {
                if (hcls.scrollIntoViewIfNeeded)
                    hcls.scrollIntoViewIfNeeded();
                else
                    hcls.scrollIntoView();
            }

        });
}

//Hide Alert
$("button.showhide").click(function () {

    if ($.trim($(this).text()) === 'Show Code') {
        $(this).text('Hide Code');
    } else {
        $(this).text('Show Code');
    }

});

//expand and collapse issues
$(".excp").on('click', function (event) {
    $(this).children('.tim-icons').toggleClass('icon-minimal-down icon-minimal-right');
});



//Revert
window.revert = function (scan_hash, finding_hash) {
    $.post("/revert", {
        scan_hash: scan_hash,
        finding_hash: finding_hash
    },
        function (result) {
            $('#revert_modal').modal('hide');
            if (result.status === "ok") {
                setTimeout(function () {
                    $.bootstrapGrowl("Moved back to issues!", {
                        type: 'success'
                    });
                }, 1000);
                setTimeout(function () {
                    $('.rid-' + finding_hash).hide();
                }, 3000);

            } else {
                setTimeout(function () {
                    $.bootstrapGrowl(result.message, {
                        type: 'danger'
                    });
                }, 1000);
            }

        });
}
//Mark as fp/na
    window.move_issue = function (scan_hash, id, issue_type) {
    var url, msg, modl;
    if (issue_type === 'fp') {
        url = '/false_positive';
        msg = 'Marked as False Positive!';
        modl = '#fp_modal'
    } else {
        url = '/not_applicable';
        msg = 'Marked as Not Applicable!';
        modl = '#na_modal'
    }
    $.post(url, {
        scan_hash: scan_hash,
        id: id
    },
        function (result) {
            $(modl).modal('hide');
            if (result.status === "ok") {
                setTimeout(function () {
                    $.bootstrapGrowl(msg, {
                        type: 'success'
                    });
                }, 1000);
                setTimeout(function () {
                    $('.id-' + id).hide();
                }, 2000);

            } else {
                setTimeout(function () {
                    $.bootstrapGrowl(result.message, {
                        type: 'danger'
                    });
                }, 1000);
            }

        });
}

//Delete Scan 
    window.delete_scan = function (scan_hash) {
        $.post('/delete_scan', {
            scan_hash: scan_hash
        },
            function (result) {
                $('#delmdl').modal('hide');
                if (result.status === "ok") {
                    setTimeout(function () {
                        $.bootstrapGrowl("Scan Deleted!", {
                            type: 'success'
                        });
                    }, 1000);
                    setTimeout(function () {
                        location.reload();
                    }, 2000);

                } else {
                    setTimeout(function () {
                        $.bootstrapGrowl(result.message, {
                            type: 'danger'
                        });
                    }, 1000);
                }

            });
    }
});

