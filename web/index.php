<?php
use \balrok\web_video\web\Gallery;

$abs_url = "http" . (($_SERVER['SERVER_PORT'] == 443) ? "s://" : "://") . $_SERVER['HTTP_HOST'].'/';

// display a single gallery
if (isset($_GET['gal'])) {
    $gal = new Gallery($_GET['gal'], "galleries");
    include "view_gallery.php";


// galleries listing
} else {
    $galleries = [];
    foreach (new DirectoryIterator("./galleries") as $fileInfo) {
        if($fileInfo->isDot()) continue;
        if($fileInfo->isDir()) {
            $g = new Gallery((string)$fileInfo, "galleries");
            if (empty($g->errors))
                $galleries[] = $g;
            else
                die(implode("<br/>\n", $g->errors));
        }
    }
    include "view_galleries.php";
}
