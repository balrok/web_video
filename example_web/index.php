<?php
include "Gallery.php";


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
            $galleries[] = $g;
        }
    }
    include "view_galleries.php";
}
