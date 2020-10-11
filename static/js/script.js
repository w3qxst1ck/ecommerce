$(document).on('click', '[data-toggle="lightbox"]', function(event) {
                event.preventDefault();
                $(this).ekkoLightbox();
            });


function ajaxSend(url, params) {
	fetch(`/${url}?${params}`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
		},
	})
}

const forms = document.querySelector('form[name=filter]');

froms.addEventListener('submit', function {
	let url = tis.action;
	let params = new URLSearchParams(new FormData(this)).toString();
	ajaxSend(url, params);
});