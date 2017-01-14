<?php
include "Element.php";

class Gallery
{
	public $folder;
	public $title;
	public $descr = '';
	public $dir;
	public $elements = [];

	public function __construct(string $folder, string $dir) {
		$dir .= '/'.$folder;
		$this->folder = $folder;
		if (!file_exists($dir) || !is_dir($dir) || strpos($dir, '..') == -1) {
			echo 'strange directory '.$dir;
			return NULL;
		}

		$this->dir = $dir;

		if (!$this->readInfo()) {
			echo "Missing info.txt file in: ".$this->dir;
			return null;
		}
		$this->readFiles();
	}

	public function readInfo() {
		if (file_exists($this->dir.'/info.txt')) {
			$info = @fopen($this->dir.'/info.txt', "r");
			if ($info)
			{
				$content = '';
				while (!feof($info))
					$content .= fgets($info, 4096);
				$rows = explode("\n", $content);
			}
			$this->title = $rows[0];
            unset($rows[0]);
			$this->descr = implode("<br/>\n", $rows);
		} else {
			return false;
		}
		return true;
	}

	public function readFiles() {
		$dir_handle = opendir($this->dir);
		$files = array();
		while ($file = readdir($dir_handle)) {
			if ($this->is_pic($file) || $this->is_video_folder($file)) {
				$files[] = $file;
			}
		}
		sort($files);
		for ($i = 0; $i < count($files); ++$i)
		{
            $type = $this->is_pic($files[$i])?'pic':($this->is_video_folder($files[$i])?'video':'');
			$this->elements[] = new Element($files[$i], $this->dir, $type);
		}
	}

	protected function isEnabled($i, $file) {
		return true;
	}

	protected function getFileDescription($i, $file) {
		return "";
	}

	public function is_pic($file) {
        if (file_exists($this->dir.'/'.$file.'/256.jpg'))
            return true;
		$ending = strtolower(substr($file, -3));
		return in_array($ending, array('jpg', 'png', 'gif'));
	}
	public function is_video_folder($file) {
		return file_exists($this->dir.'/'.$file.'/img_3.jpg');
	}

    public function getImage($type="256x") {
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

    public function getSprite() {
        foreach ($this->elements as $el) {
            if ($el->type == 'video' && $el->sprite) {
                return $el->sprite;
            }
        }
        return false;
    }

}
