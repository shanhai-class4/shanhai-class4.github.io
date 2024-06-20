function get_value()
{
	var title = document.getElementById("title").value;
	var father = document.getElementById("father").value;
	var subject = document.getElementById("subject").value;
	var csee = document.getElementById("csee").value;
	var text = document.getElementById("textarea").value;
	return {"title": title, "father": father, "subject": subject, "csee": csee, "text": text};
}
function save()
{
	var data = get_value();
	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/discuss/new/handle/save/', true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.send(JSON.stringify(data));

	xhr.onload = function() {
 		if (xhr.status == 200) {
    			window.location.href = xhr.responseText;
  		} else if (xhr.status == 500){
			alert("请检查输入的父讨论id，可见用户id是否正确");
} else {
    			console.log('Error: ' + xhr.status);
 		}
	};
}
function render()
{
	var data = get_value();
	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/discuss/new/handle/render/', true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.send(JSON.stringify(data));

	xhr.onload = function() {
 		if (xhr.status == 200) {
    			window.location.href = xhr.responseText;
  		} else if (xhr.status == 500){
			alert("请检查输入的父讨论id，可见用户id是否正确");
} else {
    			console.log('Error: ' + xhr.status);
 		}
	};
}
function publish()
{
	var data = get_value();
	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/discuss/new/handle/publish/', true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.send(JSON.stringify(data));

	xhr.onload = function() {
 		if (xhr.status == 200) {
    			window.location.href = xhr.responseText;
alert("发布成功，请等待管理员审核！");
  		} else if (xhr.status == 500){
			alert("请检查输入的父讨论id，可见用户id是否正确");
} else {
    			console.log('Error: ' + xhr.status);
 		}
	};
}