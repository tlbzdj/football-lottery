/**
 * Created by Administrator on 2015/1/3.
 */

$(document).ready(function() {
	$('.analyze').each(function(){
		if ($(this).siblings().filter('.result').text() == $(this).text())
		{
			$(this).css("background-color","PaleGreen");
		}
	});
	$('.willianTable').each(function(){
		var allTd=$(this).find('td');
		tmp=[allTd[0],allTd[1],allTd[2]];
		for(var i=1;i< allTd.length/3;i++){
			if(parseFloat(allTd[i*3]) > parseFloat(tmp[0])){
				allTd[i*3].addClass('redTd');
			}else if(parseFloat(allTd[i*3]) < parseFloat(tmp[0])){
				allTd[i*3].addClass('greenTd');
			}
			if(parseFloat(allTd[i*3+1]) > parseFloat(tmp[1])){
				allTd[i*3+1].addClass('redTd');
			}else if(parseFloat(allTd[i*3+1]) < parseFloat(tmp[1])){
				allTd[i*3+1].addClass('greenTd');
			}
			if(parseFloat(allTd[i*3+2]) > parseFloat(tmp[2])){
				allTd[i*3+2].addClass('redTd');
			}else if(parseFloat(allTd[i*3+2]) < parseFloat(tmp[2])){
				allTd[i*3+2].addClass('greenTd');
			}
			tmp=[allTd[i*3],allTd[i*3+1],allTd[i*3+2]];
		}
	});
});
