$(function () {
    // Set the height of each page
    $(".how-old-page").css("height", $(window).height());
    // Set the target action of the form
    $("#how_old_url").attr("action", $CONFIG['fisher']);
    // Set the configurations of the dropzone
    Dropzone.options.howOldDropZone = {
        url: $CONFIG['fisher'],
        uploadMultiple: false, // Only accept one file
        maxFilesize: 1, // in MB
        filesizeBase: 1000,
        dictDefaultMessage: '<h1><span class="glyphicon glyphicon-picture"></span>' +
        '<br /><small>~ Drop Your Photo Here ~</small></h1>',
        acceptedFiles: "image/jpeg", // MIME type. JPG only
        accept: function (file, done) {
            if (file.name == "justinbieber.jpg") {
                done("Naha, you don't.");
            }
            else {
                done();
            }
        }
    };
})