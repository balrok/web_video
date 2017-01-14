<?php
namespace balrok\web_video\web;

class Element
{
	public $item;  // @var string                                     // path to the element
	public $name;  // @var string
	public $sprite;
	public $type = 'pic';

	public function __construct(string $file, string $dir, string $type)
	{
		$this->name = $file;
        $this->dir = $dir;
        $this->type = $type;

		$this->item = $dir.'/'.$file;
		$this->thumb= $this->item;
		$this->sprite = '';
		if (file_exists($dir.'/'.$this->name.'/sprite.jpg'))
			$this->sprite = $dir.'/'.$this->name.'/sprite.jpg';
	}

	public function getImage($type="") {
		if ($this->type == 'pic') {
            if ($type == "")
                $type = "2048";
            if (is_dir($this->item) && file_exists($this->item . '/'. $type . ".jpg"))
                return $this->item . '/' . $type . ".jpg";
			return $this->item;
        } else if ($this->type == 'video')
			return $this->item.'/img_3.jpg';
		return false;
	}
}
