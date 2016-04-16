$(function () {
    // Set the height of each page
    $(".how-old-page").css("height", $(window).height());

    // Only show the first page
    $('.how-old-page').hide();
    $('.how-old-page').removeClass("hidden");
    $('#how-old-init-zone').show();

    // Load the data

    $.ajax({
        type: "GET",
        url: $CONFIG['review_data'],
        success: function (result, status, xhr) {
            var data = JSON.parse(result);
            if (data.success == true) {
                $('#how-old_picture-area-picture').attr('src', $CONFIG['face'] + data.message.id + '.jpg');
                $('#how-old-feedback-data-face-id').val(data.message.id);
                $('#how-old-feedback-data-face-sex').val(data.message.sex);
                $('#how-old-feedback-data-face-age').val(data.message.age);
                $('#how-old-feedback-data-face-smile').val(data.message.smile);

                $('.how-old-page').hide();
                $('#how-old-preview-zone').show();
            } else {
                doProcessError("No face left", "Thanks! Please close this page!");
            }
        }
    });

    // Try again (refresh the page)
    $('.retry-button').click(function () {
        window.location.reload();
    });

    // Show the success page
    function doProcessSuccess() {
        $('.how-old-page').hide();
        $('#how-old-success-zone').show();
    }

    // Show the error page
    function doProcessError(message, tip) {
        $('.how-old-page').hide();
        $('#how-old-error-zone').show();
        $('#how-old-error-zone-error-message').text(message);
        $('#how-old-error-zone-error-tip').text(tip);
    }

    // Feedback submit
    $("#how-old-feedback-submit").click(function () {
        var params = $("#how-old-feedback-form").serialize();
        $.ajax({
            type: 'POST',
            url: $CONFIG['feedback'],
            data: params,
            success: function (result, status, xhr) {
                var data = JSON.parse(result);
                if (data.success == true) {
                    doProcessSuccess();
                } else {
                    doProcessError(data.message, "Try again?");
                }
            },
            error: function (xhr, info, e) {
                doProcessError(e, "Try again?");
            }
        });
    });
});