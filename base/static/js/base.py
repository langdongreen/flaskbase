//
//Update text in sample collar
//
var tc = 'Black'


function update_text(){
	//update_price()
	var message = document.getElementById('text_id').value;

	if (message.length <= 10){
		document.getElementById('text').style.fontSize = '3.5em';
		//document.getElementById('vtext').style.fontSize = '3.5em';
	}
	if (message.length > 13){
		document.getElementById('text').style.fontSize = '3em';
		//document.getElementById('vtext').style.fontSize = '3em';
	}
	if (message.length > 16){
		document.getElementById('text').style.fontSize = '2.5em';
		//document.getElementById('vtext').style.fontSize = '2.5em';
	}
	if (message.length > 19){
		document.getElementById('text').style.fontSize = '2em';
		//document.getElementById('vtext').style.fontSize = '2em';
	}
	if (message.length > 23){
		document.getElementById('text').style.fontSize = '1.5em';
		//document.getElementById('vtext').style.fontSize = '1.5em';
	}

	document.getElementById('text').innerHTML = message;
	//document.getElementById('vtext').innerHTML = message;

	update_session('create/text/'+message);

}

//
//Change text colour in sample collar
//
function update_text_colour(colour,hex,icon,url){

	document.getElementById('text').style.color = hex;
	//document.getElementById('vtext').style.color = hex;


		update_session(url);
		update_icon_colour(icon,colour,hex);
		tc = colour;

}

//
//Change collar image depending on colour selected
//
function update_collar(colour,url){

	if(colour == ''){
		colour = 'black';
	}

	background = "url('static/images/"+colour+".jpg') right";

	document.getElementById('collar').style.background = background;
	//document.getElementById('vcollar').style.background = background;

	update_session(url);

}

//
//Change iconimage depending on colour selected
//
function update_icon(icon,url){

	update_session(url);
	colour = tc.toLowerCase();

	if(icon) {
   document.getElementById('icon').src = "static/images/icons/"+colour+"/"+icon+".png";
   document.getElementById('icon1').src = "static/images/icons/"+colour+"/"+icon+".png";
	 //document.getElementById('vicon').src = "static/images/icons/"+colour+"/"+icon+".png";
	 //document.getElementById('vicon1').src = "static/images/icons/"+colour+"/"+icon+".png";
 }
 else{
	 document.getElementById('icon').src = "data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==";
	 document.getElementById('icon1').src = "data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==";
	 //document.getElementById('vicon').src = "data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==";
	 //document.getElementById('vicon1').src = "data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==";
 }

}

//
//change icon colour
//
function update_icon_colour(icon,colour,hex){

		colour = colour.toLowerCase();
	 document.getElementById('icon').src = "static/images/icons/"+colour+"/"+icon+".png";
   document.getElementById('icon1').src = "static/images/icons/"+colour+"/"+icon+".png";
	 //document.getElementById('vicon').src = "static/images/icons/"+colour+"/"+icon+".png";
	 //document.getElementById('vicon1').src = "static/images/icons/"+colour+"/"+icon+".png";

	 update_class('icons','background-color: '+hex);
	}


//
//Change buckle choice and update update_session
//
function update_buckle(buckle,url){
	update_session(url);

	update_class('buckles','');

	document.getElementById(buckle).style = 'border: 2px solid black';
}

//
//Change hardware choice and update update_session
//
function update_hardware(hardware,url){
	update_session(url);

	update_class('hardware','');

	var src = "static/images/"+hardware.toLowerCase()+'.png';

	document.getElementById(hardware).style = 'border: 2px solid black';
	document.getElementById('dring').src = src;
	//document.getElementById('vdring').src = src;
}
//
//Update the style by class
//
function update_class(cssclass,style){
	var c = document.getElementsByClassName(cssclass);
	var i;

	for (i = 0; i < c.length; i++) {
		c[i].style = style;
	}
}

function add_class(cssclass,newclass){
	var c = document.getElementsByClassName(cssclass);
	var i;

	for (i = 0; i < c.length; i++) {
		c[i].classList.add(newclass);
	}
}
/*function update_all(){
	//update_icon_colour()
	update_icon();
	update_collar();
	update_text();
	update_text_colour();
}
*/

//
//Hide elements that work with javascript
//
function javascript_enabled(){
		add_class('js','inline')
}

window.onload = javascript_enabled;



//
//Get page to update session variables
//
function update_session(url){
	out = fetch(url,{credentials: 'same-origin'});

	out.then(response => response.text()) // 1
		 .then(json => {                    // 2
				console.log(json);
		 })
		 .catch(error => {                  // 3
					// handle error
		 });


}
/*var text_colour = document.getElementById('tcolour').value;

//
//Update price based on Width and Message
//
function update_price(){
	var width = document.getElementById('width').value;
	var message = document.getElementById('message').value;
	var price = 0

	if (width=='15'){
		price = 19
	}
	else if(width == '19'){
		price = 24
	}
	else if(width == '25'){
		price = 29
	}
	else {
		price = 19
	}

	if (!message){
		price = price - 5
	}

	price = '$'+price+'.00'

	document.getElementById('price').innerHTML = price;
}


//
//Update price based on Straps and Message and Hardware
//
function update_lprice(){
	var straps = document.getElementById('straps').value;
	var message = document.getElementById('message').value;
	var hardware = document.getElementById('hardware').value;
	var price = 30

	price = price + (straps * 11)

	if (!message){
		price = price - 5
	}

	if (hardware == 'brass'){
		price = price + 3
	}

	price = '$'+price+'.00'

	document.getElementById('lprice').innerHTML = price;
}

//
//Update shipping and total based on selected shipping
//
function update_shipping(){
	var sub_total = document.getElementById('sub').innerHTML;
	var shipping = document.getElementById('shipping').value;
	var price = 0

	if (shipping =='express'){
		price = 10
	}
	else if(shipping == 'standard'){
		price = 8
	}
	var total = parseInt(price)+parseInt(sub_total)

	total = '$'+total+'.00'
	document.getElementById('total').innerHTML = total;
	price = '$'+price+'.00'
	document.getElementById('postage').innerHTML = price;
}



//
//Update text in sample leash
//
function update_ltext(){
	update_lprice()
	var message = document.getElementById('message').value
	document.getElementById('text').innerHTML = message;
}
//
//Change collar image depending on colour selected
//
function update_collar(){

	var colour = document.getElementById('ccolour').value;

	switch (colour) {
            case ("red"):
                document.sample.src = "images/red.jpg";
                break;
            case ("blue"):
                document.sample.src = "images/blue.jpg";
                break;
           	case ("black"):
                document.sample.src = "images/black.jpg";
                break;
           	case ("pink"):
                document.sample.src = "images/pink.jpg";
                break;
            case ("purple"):
                document.sample.src = "images/purple.jpg";
                break;
	}

}

//Change collar image depending on colour selected
//
function update_icon(){

	var icon = document.getElementById('icon').value;

   document.icon.src = "images/icons/"+text_colour+"/"+icon+".png";
   document.icon2.src = "images/icons/"+text_colour+"/"+icon+".png";


}

//
//
function update_icon_colour(){
	var icon = document.getElementById('icon').value;
	var colour = document.getElementById('icolour').value;

	document.icon.src = "images/icons/"+colour+"/"+icon+".png";
   document.icon2.src = "images/icons/"+colour+"/"+icon+".png";
	}
//
//Change text colour in sample collar
//
function update_text_colour(){

	var colour = document.getElementById('tcolour').value;
	var text = '';
	text_colour = colour;

	update_icon();

	switch (colour) {
            case ("white"):
                text = '#FFFFFF';
                break;
        case ("red"):
                text = '#9F0606';
                break;
  	     case ("blue"):
                text = '#261A98';
                break;
        case ("ltblue"):
             text = '#17BBCF';
             break;
   		case ("black"):
                text = '#000000';
                break;
       	case ("pink"):
                text = '#C60090';
                break;
   			case ("purple"):
                text = '#690A74';
                break;
           case ("orange"):
                text = '#FF5B01';
                break;
   			case ("green"):
                text = '#0C7625';
                break;
             case ("glow"):
                text = '#FEDCFF';
                break;
	}

	document.getElementById('text').style.color = text
}
*/
