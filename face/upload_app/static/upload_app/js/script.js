
$(document).ready(function () {

	console.log("ready DOMMM");

	// const progressBox = document.getElementById('progress-box')
	const btn_submit = document.getElementById('btn_submit')
	const csrf = document.getElementsByName('csrfmiddlewaretoken')
	console.log(csrf[0].value)
	const id = document.getElementById('id')
	const name = document.getElementById('name')
	const password = document.getElementById('password')
	const uploadForm = document.getElementById('uplForm')
	// const bar = document.getElementsByClassName('processing_bar')
	const error_msg = document.getElementsByClassName('error_msg')
	// const status_bar = document.getElementsByClassName('status_uploading')
	document.getElementById('spinner').style.display = 'none'
	// status_bar[0].style.width = 50+'%';
	// console.log(status_bar[0].style)
	var btnUpload = $("#upload_file"),
		btnOuter = $(".button_outer");

	$('#second_step').addClass('active')

    $('.step').each(function(index, element) {
      // element == this
      $(element).not('.active').addClass('done');
      $('.done').html('<i class="icon-ok"></i>');
      if($(this).is('.active')) {
        return false;
      }
    });


	btnUpload.on("change", function (e) {
		console.log("if")
		var ext = btnUpload.val().split('.').pop().toLowerCase();
		if ($.inArray(ext, ['gif', 'png', 'jpg', 'jpeg']) == -1) {
			$(".error_msg").text("Не изображение");
		} else if (document.getElementById('upload_file').files[0].size > 10 * 1024 * 1024) {
			$(".error_msg").text("Слишком большой файл");
		}
		else {
			$(".error_msg").text("");
			const loading = document.getElementsByClassName('processing_bar')
			// btnOuter.addClass("file_uploading");
			document.getElementById('input_div').style.display = 'none'
			document.getElementById('spinner').style.display = 'block'

			const uploadedFile = e.target.files[0];
			
			const fd = new FormData;

			fd.append('csrfmiddlewaretoken', csrf[0].value)
			fd.append('upload_file', uploadedFile)
			fd.append('id', id.value)
			fd.append('name', name.value)
			fd.append('invite_code', password.value)
			//var uploadedFileURL = URL.createObjectURL(uploadedFile)
			
			$.ajax({
				type:'POST',
				url: uploadForm.action,
				enctype: 'multipart/form-data',
				data:fd,
				beforeSend: function(){
					
				},
				xhr: function(){
					const xhr = new window.XMLHttpRequest();
					xhr.upload.addEventListener('progress',e=>{
						$("#h1_text").addClass('extra_h1')
						setTimeout(function(){
							$("#h1_text").removeClass('extra_h1')
						},100)
						// console.log(e)
						// if (e.lengthComputable){
							
						// 	var percent = Math.floor(e.loaded / e.total * 100); 
						// 	if(percent==100){
						// 		percent = 89
						// 	}
						// 	console.log(percent)
						// 	console.log(loading[0].style.width)
						// 	if (percent < 90){
							
						// 	loading[0].style.width = percent + '%';
						// 	if (percent>50){
						// 		status_bar[0].style.width = percent +'%';
								
						// 	}
							
						// 	}

							
						// }
					})
					return xhr
				},
				success: function(response){
					document.getElementById('input_div').style.display = 'block'
					document.getElementById('spinner').style.display='none'
					// status_bar[0].style.width = 100 + '%';
					// console.log(response)
					

					
					

					// $("#uploaded_view").append('<img src="' + uploadedFileURL + '" />').addClass("show")
					
					$(".error_msg").text(response['msg'])
					// status_bar[0].style.display = 'none';
					if (response['result']=='ERROR'){
						// setTimeout(function () {
						// 	location.reload(false);
						// 	 },
						// 	  3000);
					
					}
					else{
						// $("#btn_submit").removeClass("btn-submit")
						btnOuter.addClass("file_uploaded");
						error_msg[0].style.color='green'
						$(".error_msg").text('Фото успешно добавлено')
						$('#second_step').removeClass('active')
					$('.step').each(function(index, element) {
						// element == this
						$(element).not('.active').addClass('done');
						$('.done').html('<i class="icon-ok"></i>');
						if($(this).is('.active')) {
						  return false;
						}
					  });
					 	if(test.reload()){
						setTimeout(function () {
							window.location('/checkin');
							 }, 2000);
						 }

						
						
					}
					
				},
				error: function(error){
					document.getElementById('input_div').style.display = 'block'
					document.getElementById('spinner').style.display='none'
					// status_bar[0].style.width = 100 + '%';
					
					// btnOuter.addClass("file_uploaded");
					// $("#uploaded_view").append('<img src="' + uploadedFileURL + '" />').addClass("show")
					// $("#btn_submit").removeClass("btn-submit")
					$(".error_msg").text('Ошибка отпраки фото на сервер')
					// setTimeout(function () {
					// 	location.reload(false);
					// 	 }, 3000);
				},
				cache: false,
				contentType:false,
				processData: false,

			})

			// setTimeout(function () {
			// 	btnOuter.addClass("file_uploaded");
			// }, 3000);
			// var uploadedFile = URL.createObjectURL(e.target.files[0]);
			// setTimeout(function () {
			// 	$("#uploaded_view").append('<img src="' + uploadedFile + '" />').addClass("show");
			// }, 3500);
			// setTimeout(function () {
			// 	$("#btn_submit").removeClass("btn-submit")
			// }, 3500);
		}
	});
	$(".file_remove").on("click", function (e) {
		$("#uploaded_view").removeClass("show");
		$("#uploaded_view").find("img").remove();
		btnOuter.removeClass("file_uploading");
		btnOuter.removeClass("file_uploaded");
		$("#btn_submit").addClass("btn-submit")
	});



	// btn_submit.addEventListener('click', () => {
		
	// })



});
