$('#carousel').on('slide.bs.carousel', function (event) {
    var $hoder = $('#carousel').find('.carousel-item'),
    $items = $(event.relatedTarget);
    var Index= $hoder.index($items);
	var dsto = document.getElementById('dsto');
	var dlsto = document.getElementById('dlsto');
	var dat;
	var linkd;
	if (Index == 0)
	{
		dat = dsto.dataset.cexFirst;
		linkd = dlsto.dataset.cexLFirst;
	}
	else if (Index == 1)
	{
		dat = dsto.dataset.cexSecond;
		linkd = dlsto.dataset.cexLSecond;
	}
	else if (Index == 2)
	{
		dat = dsto.dataset.cexThird;
		linkd = dlsto.dataset.cexLThird;
	}
	console.log(Index, dat, linkd);
    document.getElementById('cex_word').innerHTML = dat;
    document.getElementById('cex_link').href = linkd;
});