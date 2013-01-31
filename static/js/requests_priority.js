$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});


function reducePriority(obj, id) {
	$.ajax({
		type:		"POST",
		url:		prior_change_url + "?reduce=" + id,
		data:		{
			"reduce": id
		},
		dataType:	"json",
		success:	function(data) {
			if (data['result'] == 'success') {
				$('#request'+ id).attr('class', 'label label-info');
				$('#request'+ id).text(data['new_value'])
			}
			else {
				$('#request'+ id).attr('class', 'label');
			}
		}
	})
};


function increasePriority(obj, id) {
	$.ajax({
		type:		"POST",
		url:		prior_change_url + "?increase=" + id,
		data:		{
			"increase": id
		},
		dataType:	"json",
		success:	function(data) {
			if (data['result'] == 'success') {
				$('#request'+ id).attr('class', 'label label-info');
				$('#request'+ id).text(data['new_value'])
			}
			else {
				$('#request'+ id).attr('class', 'label label-important');
			}
		}
	})
};
