<?php
namespace balrok\web_video\web;

class Gallery
{
    public $folder;
    public $title;
    public $descr = '';
    public $dir;
    public $elements = [];
    public $errors = [];
    // will search for any of these filenames - if it finds one it stops
    public $info_filenames = ["info.txt", "info"];

    public function __construct(string $folder, string $dir)
    {
        $dir .= '/'.$folder;
        $this->folder = $folder;
        if (!file_exists($dir) || !is_dir($dir) || strpos($dir, '..') == -1) {
            $this->errors[] = 'strange directory '.$dir;
            return;
        }

        $this->dir = $dir;

        if (!$this->readInfo()) {
            $this->errors[] = "Missing info (any of ".implode(", ", $this->info_filenames)." file in: ".$this->dir;
            return;
        }
        $this->readFiles();
    }

    public function readInfo()
    {
        foreach ($this->info_filenames as $name) {
            if (file_exists($this->dir.'/'.$name)) {
                $info = @fopen($this->dir.'/'.$name, "r");
                if ($info) {
                    $content = '';
                    while (!feof($info)) {
                        $content .= fgets($info, 4096);
                    }
                    $rows = explode("\n", $content);
                }
                $this->title = $rows[0];
                unset($rows[0]);
                $this->descr = implode("<br/>\n", $rows);
                return true;
            }
        }
        return false;
    }

    public function readFiles()
    {
        $dir_handle = opendir($this->dir);
        $files = array();
        while ($file = readdir($dir_handle)) {
            if ($this->is_pic($file) || $this->is_video_folder($file)) {
                $files[] = $file;
            }
        }
        sort($files);
        for ($i = 0; $i < count($files); ++$i) {
            $type = $this->is_pic($files[$i])?'pic':($this->is_video_folder($files[$i])?'video':'');
            $this->elements[] = $this->createNewElement($files[$i], $this->dir, $type);
        }
    }

    public function createNewElement(string $file, string $dir, string $type) {
        return new Element($file, $dir, $type);
    }

    protected function isEnabled($i, $file)
    {
        return true;
    }

    protected function getFileDescription($i, $file)
    {
        return "";
    }

    public function is_pic($file)
    {
        if (file_exists($this->dir.'/'.$file.'/256.jpg')) {
            return true;
        }
        $ending = strtolower(substr($file, -3));
        return in_array($ending, array('jpg', 'png', 'gif'));
    }
    public function is_video_folder($file)
    {
        return file_exists($this->dir.'/'.$file.'/img_3.jpg');
    }

    public function getImage($type="256x")
    {
        foreach ($this->elements as $el) {
            if ($el->type == 'pic') {
                return $el->getImage($type);
            }
        }
        foreach ($this->elements as $el) {
            if ($el->type == 'video') {
                return $el->getImage();
            }
        }
        return false;
    }

    public function getSprite()
    {
        foreach ($this->elements as $el) {
            if ($el->type == 'video' && $el->sprite) {
                return $el->sprite;
            }
        }
        return false;
    }
}
