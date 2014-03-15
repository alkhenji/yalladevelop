$(document).ready(function(){

});

// function deleteComment(n){
// 	location.href="delete/?cid="+n;
// }
// 
// function add(){
// 	var caption = document.getElementById("caption").value;
// 	var preview = $('#imagePreview')[0].getElementsByTagName("img")[0];
// 	if (caption==""){
// 		alert("Caption cannot be empty."); return false;
// 	} else if (preview==undefined){
// 		alert("Please chose an image to upload first."); return false;
// 	} else {
// 		var url = $("#uploaderUrl > input").val();
// 		if (checkURL(url)){
// 			location.href = "add/?caption="+caption+"&url="+url;
// 		}
// 	}
// }
// 
function postComment(){
	var comment = $("#comment").val();
	alert(comment);
	return false;
	location.href="post/?comment=" + comment;
}