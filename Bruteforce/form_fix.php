<?php
if( isset($_POST['Login']) && isset($_POST['username']) && isset($_POST['username']) ) {
	
    $user = stripslashes($_POST['username']);

    $total_failed_login = 3;  
    $lockout_time       = 5;  
    $account_locked     = false; 

    $data = $db->prepare( 'SELECT failed_login, last_login FROM users WHERE user = (:user) LIMIT 1;' );  
    $data->bindParam( ':user', $user, PDO::PARAM_STR );  
    $data->execute();  
    $row = $data->fetch();  
 
    if (($data->rowCount() == 1) && ($row['failed_login'] >= $total_failed_login)) {  
	
        $last_login = strtotime( $row[ 'last_login' ] );  
        $timeout    = $last_login + ($lockout_time * 60);  
        $timenow    = time();  

        if( $timenow < $timeout ) {  
            $account_locked = true;  
        }  
    }  

    $pass = md5( stripslashes( $_POST['password'] ) );  

    // MD5 -> SHA256 (pass + get_salt($user));

    $data = $db->prepare( 'SELECT * FROM users WHERE user = (:user) AND password = (:password) LIMIT 1;' );  
    $data->bindParam( ':user', $user, PDO::PARAM_STR);  
    $data->bindParam( ':password', $pass, PDO::PARAM_STR );  
    $data->execute();  

    $row = $data->fetch();

    $html = "";

    if( ( $data->rowCount() == 1 ) && ( $account_locked == false ) ) {  
        $avatar = $row[ 'avatar' ];  

        $html .= "<p>Welcome to the password protected area {$user}</p>";  
        $html .= "<img src=\"{$avatar}\" />";  

        $failed_login = $row[ 'failed_login' ];  
        $data = $db->prepare( 'UPDATE users SET failed_login = "0" WHERE user = (:user) LIMIT 1;' );  
        $data->bindParam( ':user', $user, PDO::PARAM_STR );  
        $data->execute();  
    } else {  
        sleep(3);  

        $html .= "<pre>";
        $html .= "Username and/or password incorrect.<br/><br/>";
        $html .= "This account has been blocked for too many login attempts.<br/>";
        $html .= "Please try again in {$lockout_time} minutes<br/>";

        $data = $db->prepare( 'UPDATE users SET failed_login = (failed_login + 1) WHERE user = (:user) LIMIT 1;' );  
        $data->bindParam( ':user', $user, PDO::PARAM_STR );  
        $data->execute();  
    }

    $data = $db->prepare( 'UPDATE users SET last_login = now() WHERE user = (:user) LIMIT 1;' );  
    $data->bindParam( ':user', $user, PDO::PARAM_STR );  
    $data->execute();
}
 
?>
