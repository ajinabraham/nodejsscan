function delete_scan(scan_hash) {
    $.post('/delete_scan', {
            scan_hash: scan_hash
        },
        function(result) {
            $('#delmdl').modal('hide');
            if (result.status === "ok") {
                setTimeout(function() {
                    $.bootstrapGrowl("Scan Deleted!", {
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