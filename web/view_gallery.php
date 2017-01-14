<?php include "view_head.php" ?>
<?php $baseUrl = "/"?>

<h2 align="center"><u><?=$gal->title?></u></h2>
<div class="gallery_elements row" style="display:flex;flex-wrap:wrap;">
<?php foreach ($gal->elements as $id=>$model) { ?>
        <div class="element_<?=$model->type?> col-xl-2 col-md-3 col-xs-6">
            <div class="card">
<table style="height:100%"><tr><td class="align-middle" style="padding:0">
    <?php if ($model->type == 'pic') {?>
        <a href="<?= $baseUrl . $model->getImage()?>" class="boxpopup">
            <img src="<?=$baseUrl.$model->getImage("x512")?>" class="card-img img-fluid" />
        </a>
<?php } else if($model->type == 'video') {?>

<?php $url = $abs_url . $model->item .'/';?>

<a href="#flowvid_<?=$id?>" class="boxpopup">
    <img src="<?=$baseUrl.$model->getImage()?>" class="card-img img-fluid" />
    <div class="after"></div>
</a>

<div class="mfp-hide flowvideo video-fluid" id="flowvid_<?=$id?>">
    <img src="<?=$baseUrl.$model->getImage()?>" style="height:100%;width:100%;" />
</div>

<script>
window.onload = function () {
  flowplayer("#flowvid_<?=$id?>", {
    autoplay: true,
    embed: false, // setup would need iframe embedding
 
    // manual HLS level selection for Drive videos
    hlsQualities: true,
 
    // manual VOD quality selection when hlsjs is not supported
    qualities: false, // if this is enabled and same as in hls it would select still mp4
    splash:true, // splash vs logo
        // logo will download the first part of an mp4 video and display a nice image
        // problem with dash,hls: it downloads the complete video
        // splash: will do nothing until play is pressed => provide our own image here
 
    clip: {
      loop: true,
      sources: [
		// first hls because it allows manual quality selection
        {type:"application/x-mpegurl",src: "<?=$url?>master.m3u8" },
		// then comes dash without manual quality selection but still good protocol
		{type:"application/dash+xml", src: "<?=$url?>stream.mpd" },
		// then mp4 because h264 is the standard and might be played nearly everywhere
		{type:"video/mp4",            src: "<?=$url?>video_02000.mp4"},
		// then webm which has bigger videos and is afaik only required for older opera browsers
		{type:"video/webm",           src: "<?=$url?>video.webm"}
      ]
    }
 
  });
};
</script>























<?php } ?>



</td></tr></table>
            </div>
        </div>
<?php } ?>
</div>
<?=$gal->descr?>

<br/><br/>
<?php include "view_foot.php" ?>
