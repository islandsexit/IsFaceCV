
$(document).ready(function () {
	console.log("ready DOM");

	const progressBox = document.getElementById('progress-box')
	const btn_submit = document.getElementById('btn_submit')
	const csrf = document.getElementsByName('csrfmiddlewaretoken')
	const id = document.getElementById('id')
	const name = document.getElementById('name')
	const password = document.getElementById('password')
	const uploadForm = document.getElementById('uplForm')
	const bar = document.getElementsByClassName('processing_bar')
	const error_msg = document.getElementsByClassName('error_msg')


	var btnUpload = $("#upload_file"),
		btnOuter = $(".button_outer");
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

			btnOuter.addClass("file_uploading");
			const loading = document.getElementsByClassName('processing_bar')

			const uploadedFile = e.target.files[0];
			
			const fd = new FormData;

			fd.append('csrfmiddlewaretoken', csrf[0].value)
			fd.append('upload_file', uploadedFile)
			fd.append('id', id.value)
			fd.append('name', name.value)
			fd.append('password', password.value)
			var uploadedFileURL = URL.createObjectURL(uploadedFile)
			
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
						// console.log(e)
						if (e.lengthComputable){
							
							var percent = Math.floor(e.loaded / e.total * 100); 
							if(percent==100){
								percent = 89
							}
							console.log(percent)
							console.log(loading[0].style.width)
							if (percent < 90){
							
							loading[0].style.width = percent + '%';
							
							}
							
						}
					})
					return xhr
				},
				success: function(response){
					loading[0].style.width = 100 + '%';
					console.log(response)
					btnOuter.addClass("file_uploaded");
					// $("#uploaded_view").append('<img src="' + uploadedFileURL + '" />').addClass("show")
					$("#btn_submit").removeClass("btn-submit")
					$(".error_msg").text(response['msg'])
					if (response['result']=='ERROR'){
						setTimeout(function () {
							location.reload(false);
							 }, 2000);
					
					}
					else{
						error_msg[0].style.color='green'
						$(".error_msg").text(response['msg'])
						// setTimeout(function () {
						// 	window.location('/checkin');
						// 	 }, 2000);
						
						
					}
					
				},
				error: function(error){
					console.log(error)
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
