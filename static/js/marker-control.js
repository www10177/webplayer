// load video object
var video = videojs('mv');
video.markers({
	markers:[{time:0,text :'init'}]
});
video.markers.removeAll()

function show_time(){
	$('#currentTime').html($('#mv').find('video').get(0).currentTime);
	$('#totalTime').html($('#mv').find('video').get(0).duration);    
}
function marktime(){
	var time = $('#mv').find('video').get(0).currentTime;
	time = Math.round(time) ;
	console.log(time)
	video.markers.add([{time:time, text: time}]);
}
