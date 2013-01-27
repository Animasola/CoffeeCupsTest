function display_form_errors(errors, $form) {
	for (var error in errors) {
		$form.find('textarea[name=' + error + '], input[name=' + error + ']').after('<div class="error" style="color:#ff0000"; float:right;>' + errors[error] + '</div>');
	}
}

$(document).ready(function() {
	var options = {
		type:		'post',
		dataType:	'json',
		success:	responseShow
	};
	$('#editmyinfo').submit(function() {
		$(this).ajaxSubmit(options);
		var $form_elems = $(this).find('input, textarea, button');
		$form_elems.prop("disabled",true);
		$('#error_message').text("Loading data, it may take a few moments...").fadeIn("slow");
		return false;
	});
});
function responseShow(data, responseText, statusText, xhr, $form) {
	$('#editmyinfo').find('input, textarea, button').prop("disabled", false);
	$('#editmyinfo').find('.error').remove();
	$('#error_message').fadeOut("slow");
	if (data['result'] == 'success') {
		e_msg = 'Info successfully updated! ';
	}
	else if (data['result'] == 'error') {
		e_msg = "Your form contains errors, please check out!";
		display_form_errors(data['form_errors'], $('#editmyinfo'));
	}
	$('#error_message').text( e_msg ).fadeIn("slow");
}
