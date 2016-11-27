<?php include "view_head.php" ?>

<div class="card-columns">
    <?php foreach ($galleries as $gal) { ?>
    <div class="card">
        <div class="card-header"><a href="index.php?gal=<?=$gal->folder?>" style="display:block"><?=$gal->title?></a></div>
        <div class="<?=$gal->getSprite()?'sprite':''?>">
            <a href="index.php?gal=<?=$gal->folder?>">
                <img src="<?=$gal->getImage("x256")?>" class="img-fluid"/>
                <?php if ($gal->getSprite()) {?>
                    <div class="sprite-hover">
                        <img src="<?=$gal->getSprite()?>" />
                    </div>
                <?php } ?>
            </a>
        </div>
        <div class="card-block">
            <div class="card-text"><?= $gal->descr ?></div>
        </div>
        <div style="clear:left;"></div>
    </div>
    <?php } ?>
</div>

<?php include "view_foot.php" ?>
