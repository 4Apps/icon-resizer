
var inProgress = false;

$('#drop_files')
    .on('dragover', function(event){
        event.preventDefault();
        return false;
    })
    .on('dragenter', function(event){
        $('#drop_files').addClass('active');
    })
    .on('dragleave', function(){
        $('#drop_files').removeClass('active');
    })
    .on('drop', function(event){
        event.preventDefault();
        $('#drop_files').removeClass('active');

        var files = event.originalEvent.dataTransfer.files;
        if (files.length > 0)
        {
            if (inProgress === true)
            {
                return;
            }
            inProgress = true;


            var drop_them_here = $('#drop_them_here'),
                progress_bg = $('#progress_bg'),
                progress = $('#progress'),
                loader = $('#loader'),
                errors = $('#errors');


            errors.removeClass('noerror').html("");
            var formData = new FormData();
            formData.append('file', files[0]);


            var xhr = new XMLHttpRequest();
            xhr.open('POST', BaseUrl + 'upload');

            xhr.upload.onprogress = function(event)
            {
                if (event.lengthComputable)
                {
                    var complete = (event.loaded / event.total * 100 | 0);
                    progress.css('width', complete + '%');
                }
            };
            xhr.onerror = function()
            {
                inProgress = false;
                loader.addClass('hide');
                progress_bg.addClass('hide');
                drop_them_here.removeClass('hide');
                progress.css('width', '0%');
                errors.html("Connection error. Check if your internet just didn't go away..");
            };
            xhr.onload = function()
            {
                inProgress = false;
                loader.addClass('hide');
                progress_bg.addClass('hide');
                drop_them_here.removeClass('hide');
                progress.css('width', '0%');

                if (xhr.status === 200) 
                {
                    try{
                        response = JSON.parse(xhr.responseText);
                    }
                    catch(e){
                        errors.html("Couldn't parse response data. Please try again later or something.");
                        return;
                    }

                    if (typeof response.error != "undefined" && response.error.code != 0)
                    {
                        errors.html(response.error.msg);
                        return;
                    }

                    location.href = StaticUrl + 'icons/' + response.filename;
                    errors.addClass('noerror').html(StaticUrl + 'icons/' + response.filename);
                }
                else
                {
                    errors.html("Something went terribly wrong. Please try again later or something.");
                }
            };


            drop_them_here.addClass('hide');
            loader.removeClass('hide');
            progress_bg.removeClass('hide');
            xhr.send(formData);
        }
    
        return false;
    });


$(window)
    .on('dragover', function(event){
        event.preventDefault();
        return false;
    })
    .on('drop', function(event){
        event.preventDefault();
        return false;
    });