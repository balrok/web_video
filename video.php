<script src="flowplayer-6.0.5/flowplayer.min.js'"></script>
<script src="flowplayer-6.0.5/flowplayer.dashjs.min.js'"></script>
<script src="flowplayer-6.0.5/flowplayer.hlsjs.min.js'"></script>
<script src="flowplayer-6.0.5/flowplayer.quality-selector.min.js'"></script>
<link rel="flowplayer-6.0.5/skin/functional.css"/>
<link rel="flowplayer-6.0.5/flowplayer.quality-selector.css"/>

<div id="flowvid">
</div>

<script type="text/javascript">
window.onload = function () {
  flowplayer("#flowvid", {
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
