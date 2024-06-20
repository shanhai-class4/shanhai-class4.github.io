function accept()
{
	var xhr = new XMLHttpRequest();
	xhr.open('POST', './handle/accept/', true);
	xhr.setRequestHeader('Content-Type', 'text/plain');
	xhr.send("accept");
	xhr.onload = function() {
 		if (xhr.status == 200) {
    			window.location.href = xhr.responseText;
  		}
	};
}
function reject()
{
	var xhr = new XMLHttpRequest();
	xhr.open('POST', './handle/reject/', true);
	xhr.setRequestHeader('Content-Type', 'text/plain');
	xhr.send("reject");
	xhr.onload = function() {
 		if (xhr.status == 200) {
    			window.location.href = xhr.responseText;
  		}
	};
}
function delete()
{
	var xhr = new XMLHttpRequest();
	xhr.open('POST', './handle/delete/', true);
	xhr.setRequestHeader('Content-Type', 'text/plain');
	xhr.send("delete");
	xhr.onload = function() {
 		if (xhr.status == 200) {
    			window.location.href = xhr.responseText;
  		}
	};
}