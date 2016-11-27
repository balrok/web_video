<?php

class Element
{
	public $gallery;
	public $item;                                       // path to the element
	public $name;
	public $big;                                        // path to the big picture
	public $thumb;
	public $sprite;
	public $type = 'pic';

	public function __construct(string $file, string $dir, string $type)
	{
		$this->name = $file;
        $this->dir = $dir;
        $this->type = $type;

		$this->item = $dir.'/'.$file;
		$this->thumb= $this->item;
		$this->big= $this->item;
		$this->sprite = '';
		if (file_exists($dir.'/'.$this->name.'/sprite.jpg'))
			$this->sprite = $dir.'/'.$this->name.'/sprite.jpg';
		if (file_exists($dir.'/'.$this->name.'/x256.jpg'))
			$this->thumb = $dir.'/'.$this->name.'/x256.jpg';
		elseif (file_exists($dir.'/thumb/'.$this->name))
			$this->thumb = $dir.'/thumb/'.$this->name;
		if (file_exists($dir.'/'.$this->name.'/2048.jpg'))
			$this->big = $dir.'/'.$this->name.'/2048.jpg';
		elseif (file_exists($dir.'/big/'.$this->name))
			$this->big = $dir.'/big/'.$this->name;
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
