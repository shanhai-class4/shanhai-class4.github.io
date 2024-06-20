function Insert(textarea, textToInsert)
{
    var startPos = textarea.selectionStart;
    var endPos = textarea.selectionEnd;
    //var scrollTop = textarea.scrollTop;
    textarea.value = textarea.value.substring(0, endPos)
                    + textToInsert
                    + textarea.value.substring(endPos, textarea.value.length);
    //if (textarea.setSelectionRange) {
    //    textarea.setSelectionRange(endPos + textToInsert.length, endPos + textToInsert.length);
    //textarea.scrollTop = scrollTop;
}
function Fix(textarea, textToInsert1, textToInsert2)
{
    var startPos = textarea.selectionStart;
    var endPos = textarea.selectionEnd;
    //var scrollTop = textarea.scrollTop;
    textarea.value = textarea.value.substring(0, startPos)
                    + textToInsert1
					+ textarea.value.substring(startPos, endPos)
					+ textToInsert2
                    + textarea.value.substring(endPos, textarea.value.length);
    //if (textarea.setSelectionRange) {
    //    textarea.setSelectionRange(startPos, endPos + textToInsert1.length + textToInsert2.length);}
    //textarea.scrollTop = scrollTop;
}
function insertBold()
{
	var textarea = document.getElementById("textarea");
	var startPos = textarea.selectionStart;
    var endPos = textarea.selectionEnd;
	if (startPos == endPos) Insert(textarea, "\\*\\*需要粗体的内容\\*");
	else Fix(textarea, "\\*\\*", "\\*");
}
function insertItatic()
{
	var textarea = document.getElementById("textarea");
	var startPos = textarea.selectionStart;
    var endPos = textarea.selectionEnd;
	if (startPos == endPos) Insert(textarea, "\\?\\?需要斜体的内容\\?");
	else Fix(textarea, "\\?\\?", "\\?");
}
function insertUnderline()
{
	var textarea = document.getElementById("textarea");
	var startPos = textarea.selectionStart;
    var endPos = textarea.selectionEnd;
	if (startPos == endPos) Insert(textarea, "\\_\\_需要下划线的内容\\_");
	else Fix(textarea, "\\_\\_", "\\_");
}
function insertTitle()
{
	var textarea = document.getElementById("textarea");
	var startPos = textarea.selectionStart;
    var endPos = textarea.selectionEnd;
	if (startPos == endPos) Insert(textarea, "\\##标题内容\\@@\n");
	else Fix(textarea, "\\##", "\\@@\n");
}
function insertSTitle()
{
	var textarea = document.getElementById("textarea");
	var startPos = textarea.selectionStart;
    var endPos = textarea.selectionEnd;
	if (startPos == endPos) Insert(textarea, "\\#小标题内容\\@\n");
	else Fix(textarea, "\\#", "\\@\n");
}
function insertPicture()
{
	window.open('../../../discuss/pic_upload/', '_blank');
	var textarea = document.getElementById("textarea");
	var startPos = textarea.selectionStart;
    var endPos = textarea.selectionEnd;
	if (startPos == endPos) Insert(textarea, "\\![从图床获取的图片地址\\]\n");
	else Fix(textarea, "\\![", "\\]\n");
}
function insertLink()
{
	var textarea = document.getElementById("textarea");
	var startPos = textarea.selectionStart;
    var endPos = textarea.selectionEnd;
	if (startPos == endPos) Insert(textarea, "\\+链接地址\\-对链接地址的描述\\=");
	else Fix(textarea, "\\+", "\\-对链接地址的描述\\=");
}
function insertFile()
{
	window.open('../../../discuss/file_upload/', '_blank');
	var textarea = document.getElementById("textarea");
	var startPos = textarea.selectionStart;
    var endPos = textarea.selectionEnd;
	if (startPos == endPos) Insert(textarea, "\\/文件链接地址\\~对文件的描述\\=");
	else Fix(textarea, "\\/", "\\~对文件的描述\\=");
}
function insertMark()
{
	var textarea = document.getElementById("textarea");
	var startPos = textarea.selectionStart;
    var endPos = textarea.selectionEnd;
	if (startPos == endPos) Insert(textarea, "\\==需要高亮的内容\\=?");
	else Fix(textarea, "\\==", "\\=?");
}
function insertBlockquote() // 引用
{
	var textarea = document.getElementById("textarea");
	var startPos = textarea.selectionStart;
    var endPos = textarea.selectionEnd;
	if (startPos == endPos) Insert(textarea, "\\>需要引用的内容\\>>");
	else Fix(textarea, "\\>", "\\>>");
}