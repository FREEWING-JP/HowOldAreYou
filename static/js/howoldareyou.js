$(function () {
    // Set the height of each page
    $(".how-old-page").css("height", $(window).height());

    // Set the target action of the form
    $("#how_old_url").attr("action", $CONFIG['fisher']);

    // Only show the first page
    $('.how-old-page').hide();
    $('.how-old-page').removeClass("hidden");
    $('#how-old-init-zone').show();

    // Try again (refresh the page)
    $('.retry-button').click(function () {
        window.location.reload();
    });

    // Show the waiting page
    function doWaiting() {
        $('.how-old-page').hide();
        $('#how-old-waiting-zone').show();
    }

    // Change the smile degree into string
    function doSmileString(degree) {
        var sentence = {
            0: ['Why are you so sad?'],
            1: ['Just be happy!'],
            2: ['Smile~'],
            3: ['You are SO happy~'],
            4: ['What a big laugh!', 'LOL', 'Laugh out loudly!']
        };
        var degreeInt = Math.floor(degree / 20);
        var arr = sentence[degreeInt];
        var str = arr[Math.floor(Math.random() * arr.length)];
        return str;
    }

    // Show the error page
    function doProcessError(message, tip) {
        $('.how-old-page').hide();
        $('#how-old-error-zone').show();
        $('#how-old-error-zone-error-message').text(message);
        $('#how-old-error-zone-error-tip').text(tip);
    }

    // Show the result page
    function doShowFace(data) {
        $('.how-old-page').hide();
        $('#how-old-preview-zone').show();
        var pic_id = data.pic_id;
        var n_faces = data.n_faces;
        var height = data.height;
        var width = data.width;
        var container = $('#how-old-picture-wrapper');
        var imgPhoto = $('#how-old_picture-area-picture');
        var scale = imgPhoto.width / width;
        $('#how-old_picture-area-picture').attr('src', $CONFIG['photo'] + data.pic_id + '.jpg');
        $.each(data.faces, function (ith, face) {
            var toolTip = $('<div></div>').addClass("media");
            var toolTipLeft = $('<div></div>').addClass("media-left").addClass("media-middle");
            var toolTipLeftPicture = $("<img />");
            switch (face.sex.value) {
                case 0:
                    toolTipLeftPicture.attr("src", $CONFIG['image_sex_female']);
                    break;
                case 1:
                    toolTipLeftPicture.attr("src", $CONFIG['image_sex_male']);
                    break;
                default:
                    toolTipLeftPicture.attr("src", $CONFIG['image_sex_male']);
            }
            var toolTipRight = $('<div></div>').addClass("media-body");
            var toolTipRightAge = $('<h3></h3>').addClass("media-heading").html(Math.round(face.age.value));
            toolTipRight.append(toolTipRightAge);
            var toolTipRightSmile = $('<div></div>').html(doSmileString(face.smile.value));
            toolTipRight.append(toolTipRightSmile);
            toolTipLeft.append(toolTipLeftPicture);
            toolTip.append(toolTipLeft);
            toolTip.append(toolTipRight);

            var top = (face.top / height) * 100;        //scale * face.top;
            var bottom = (face.bottom / height) * 100;  //scale * face.bottom;
            var left = (face.left / width) * 100;       //scale * face.left;
            var right = (face.right / width) * 100;     //scale * face.right;
            // Make a face rectangle
            var faceElement = $("<div></div>");
            faceElement.addClass('how-old-face-rectangle');
            faceElement.attr('id', 'how-old-face-rectangle-' + ith);
            faceElement.attr('data-toggle', 'tooltip');
            faceElement.attr('data-placement', 'top');
            faceElement.attr('data-face-id', face.id);
            faceElement.attr('data-face-sex', face.sex.value);
            faceElement.attr('data-face-age', face.age.value);
            faceElement.attr('data-face-smile', face.smile.value);
            faceElement.attr('title', toolTip.html());
            faceElement.css('position', 'absolute');
            faceElement.css('left', (left) + '%');
            faceElement.css('top', (top) + '%');
            faceElement.css('width', (right - left) + '%');
            faceElement.css('height', (bottom - top) + '%');

            // Append to the container
            container.prepend(faceElement);
        });

        $('[data-toggle="tooltip"]').tooltip({
            html: true
        });

        $('.how-old-face-rectangle').click(function () {
            $('#how-old-feedback-data-face-id').val($(this).data('face-id'));
            $('#how-old-feedback-data-face-sex').val($(this).data('face-sex'));
            $('#how-old-feedback-data-face-age').val(Math.round($(this).data('face-age')));
            $('#how-old-feedback-data-face-smile').val(Math.round($(this).data('face-smile')));
            $('#how-old-feedback').modal();
            $('.how-old-feedback-element').hide();
            $('#how-old-feedback-main').show();
            $('#how-old-feedback-control').show();
        });
    }

    // Judge if it's really success
    function doProcessSuccess(data) {
        if (data.success == true) {
            doShowFace(data.message);
        } else {
            doProcessError(data.message, data.tip);
        }
    }

    // Set the configurations of the dropzone
    Dropzone.options.howOldDropZone = {
        url: $CONFIG['fisher'],
        uploadMultiple: false, // Only accept one file
        maxFilesize: 3, // in MB
        filesizeBase: 1024,
        dictDefaultMessage: '<h1><span class="glyphicon glyphicon-picture"></span>' +
        '<br /><small>~ Drop Your Photo Here ~</small></h1>',
        acceptedFiles: "image/jpeg", // MIME type. JPG only
        sending: function (foo, xhr, formData) {
            doWaiting();
        },
        error: function (foo, response) {
            doProcessError(response, "Try again?");
        },
        success: function (foo, response) {
            var data = JSON.parse(response);
            doProcessSuccess(data);
        }
    };

    // Set the configurations of the ajax
    $("#how_old_url_submit").click(function () {
        var params = $("#how_old_url").serialize();
        $.ajax({
            type: 'POST',
            url: $CONFIG['fisher'],
            data: params,
            beforeSend: function (xhr) {
                doWaiting();
            },
            success: function (result, status, xhr) {
                var data = JSON.parse(result);
                doProcessSuccess(data);
            },
            error: function (xhr, info, e) {
                doProcessError(info, 'Try again?');
            }
        });
    });

    function doFeedbackSuccess() {
        $('.how-old-feedback-element').hide();
        $('#how-old-feedback-success').show();
    }

    function doFeedbackError() {
        $('.how-old-feedback-element').hide();
        $('#how-old-feedback-error').show();
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
                    doFeedbackSuccess()
                } else {
                    doFeedbackError()
                }

            },
            error: function (xhr, info, e) {
                doFeedbackSuccess()
            }
        });
    });
});