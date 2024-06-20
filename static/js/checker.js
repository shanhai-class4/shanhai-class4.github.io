function check()
{
	refreshColor();
	//console.log("Checked 1000ms");
				
	setTimeout('check()', 1000);
}

window.onload = function()
{
	check();
};