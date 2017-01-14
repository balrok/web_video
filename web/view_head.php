<!doctype html>
<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0-alpha.5/css/bootstrap.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/magnific-popup.js/1.1.0/magnific-popup.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.4/jquery.min.js" type="text/javascript"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/magnific-popup.js/1.1.0/jquery.magnific-popup.min.js" type="text/javascript"></script>


<script src="/flowplayer-6.0.5/flowplayer.min.js"></script>
<script src="/flowplayer-6.0.5/flowplayer.dashjs.min.js"></script>
<script src="/flowplayer-6.0.5/flowplayer.hlsjs.min.js"></script>
<script src="/flowplayer-6.0.5/flowplayer.quality-selector.min.js"></script>
<link rel="stylesheet" href="/flowplayer-6.0.5/skin/functional.css">
<link rel="stylesheet" href="/flowplayer-6.0.5/flowplayer.quality-selector.css">

<script>
jQuery(function() {
jQuery('.boxpopup').magnificPopup({
  type: 'image',
  gallery:{
	enabled:true
  },
  closeBtnInside:false,
  callbacks: {
    elementParse: function(item) {
      if (item.src.charAt(0) == '#') {
         item.type = 'inline';
      } else {
         item.type = 'image';
      }
    },
    change: function() {
      var item = this.currItem;
      if (item.src.charAt(0) == '#') {
        // I guess a small timeout is needed so the popup can copy the dom-elements over
        window.setTimeout(function(){
            flowplayer($(item.src)).load();
        }, 100);
      }
    },
  }
});
});
</script>

<script>
jQuery(function() {
var sprite_pos = 9;
var sprite_interval = 0;
jQuery(".sprite").hover(function(){
	var s = jQuery(this).find("div.sprite-hover")
	s.show();
	function up() {
		if (++sprite_pos == 10) { sprite_pos = 0; }
		s.find("img").css("margin-left", (-100 * sprite_pos) + "%");
	}
    up();
	sprite_interval = window.setInterval(up, 1000);
}, function() {
	sprite_pos = 9;
	window.clearInterval(sprite_interval);
	sprite_intervall = 0;
	jQuery(this).find("div.sprite-hover").hide();
});
});
</script>
<style>
.sprite {
	position: relative;
	overflow: hidden;
}
.sprite-hover {
	position: absolute;
	top: 0;
	left: 0;
	display: none;
	overflow: hidden;
	background-color:#fff;
	height:100%;
}
.sprite-hover img {
	width: 1000% !important; /* 10 images = 10*100% */
}
.card-text {
	font-size:0.8em;
	line-height:1.2;
}

h1 {
	text-transform:uppercase;
	font-size:1.5rem;
}


.card {
  position: relative;
  display: block;
  margin-bottom: 0.75rem;
  background-color: #fff;
  border-radius: 0.25rem;
  border: 1px solid rgba(0, 0, 0, 0.125);
}
.card-header {
  padding: 0.75rem 1.25rem;
  margin-bottom: 0;
  background-color: #f5f5f5;
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}

.card-header::after {
  content: "";
  display: table;
  clear: both;
}

.card-img-left {
  border-bottom-left-radius: calc(0.25rem - 1px);
  border-top-left-radius: calc(0.25rem - 1px);
}
.card-img-right{
  border-bottom-right-radius: calc(0.25rem - 1px);
  border-top-right-radius: calc(0.25rem - 1px);
}
/*
// xs
// sm @media (min-width: 576px) {
// md @media (min-width: 768px) {
// lg @media (min-width: 992px) {
// xl @media (min-width: 1200px) {
*/

.card-columns .card .card-block {
    padding-bottom: 0;
    padding-top: 0.3rem;
    padding-left: 0.5rem;
    overflow:hidden;
}
.card-columns .card img {
    width:50%;
    float:left;
}
@media (min-width: 576px) {
    .card-columns .card .card-block {
        padding: 0.7rem;
        overflow:auto;
    }
    .card-columns .card img {
        width:100%;
        float:none;
    }

  .card-columns {
    -webkit-column-count: 2;
       -moz-column-count: 2;
            column-count: 2;
    -webkit-column-gap: 0.8rem;
       -moz-column-gap: 0.8rem;
            column-gap: 0.8rem;
  }
  .card-columns .card {
    display: inline-block;
    width: 100%;
  }
}
@media (min-width: 768px) {
  .card-columns {
    -webkit-column-count: 3;
       -moz-column-count: 3;
            column-count: 3;
    -webkit-column-gap: 0.95rem;
       -moz-column-gap: 0.95rem;
            column-gap: 0.95rem;
  }
  .card-columns .card {
    display: inline-block;
    width: 100%;
  }
}

.gallery_elements.row > div[class*='col-'] {display: flex;flex:1 0 auto;}
</style>




</head>
<body>
<div class="container">
<nav class="navbar navbar-light bg-faded">
  <a class="navbar-brand" href="/index.php">Index</a>
</nav>
<br/>

