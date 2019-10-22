Dropzone.autoDiscover = false;
$(document).ready(function() {
    $(function () {
        $('[data-toggle="popover"]').popover()
    });
    var validator = $('#converterForm').validate({
        rules: {
            email: {
                required: true,
                email: true
            },
            file: {
                required: true
            }
        },
        errorPlacement: function(error, element) {
            error.appendTo('.errors');
        }
    });
    new Dropzone('#fileInput', {
        url: "#",
        maxFiles:1,
        addRemoveLinks: true,
        acceptedFiles: "application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.oasis.opendocument.text,.md",
        autoProcessQueue: false,
        init: function () {
            var myDropzone = this;
            $("#submit").click(function (e) {
                e.preventDefault();
                myDropzone.processQueue();
                if(!validator.form()) {
                    alert("E' necessario fornire un indirizzo email");
                }
            });
            myDropzone.on('success', function () {
                window.location.href = window.conversionStartedLocation;
            });
        },
        sending: function (file, xhr, formData) {
            formData.append("email", $('#id_email').val());
            formData.append("monospace", $('#id_monospace').val());
            formData.append("csrfmiddlewaretoken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        dictDefaultMessage: "Trascina qui i file o clicca per caricarli",
        dictFallbackMessage: "Il tuo browser non supporta alcune funzioni di caricamento file",
        dictFallbackText: "Il file che stai provando a caricare non è supportato",
        dictFileTooBig: "Il file che stai tentando di caricare è troppo pesante",
        dictInvalidFileType: "Il file che stai provando a caricare non è supportato",
        dictResponseError: "Il server non permette il caricamento del file, prova a riaggiornare la pagina",
        dictCancelUpload: "Annulla",
        dictUploadCanceled: "Caricamento annullato",
        dictCancelUploadConfirmation: "Vuoi davvero interrompere il caricamento?",
        dictRemoveFile: "Rimuovi",
        dictMaxFilesExceeded: "Non puoi caricare altri file"
    })

    $('.it-info').on('click', function () {
        $('.it-info').not(this).popover('hide');
    })
})
