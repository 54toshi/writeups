<?php

$pw = '0e385589729688144363378792916561';  // the double hashed password

for ($i = 1; $i <= 9999999999; $i++) {
        $key_hash = md5(md5(trim($i)));
        if ($key_hash == $pw){
                echo "found collision: " . $i;
        }
}

// result:
// found collision: 179122048

?>