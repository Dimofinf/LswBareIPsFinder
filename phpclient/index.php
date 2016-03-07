<form method="POST" action="index.php" id="finder">
    <textarea style="height:200px;width:400px;" name="ips" form="finder" ></textarea>
    <input type="submit" value="Start" name="start" class="btn1">
</form>

<?php
	# Vars	
	$python_script	= "../";
	$search_pool_file = "../search_pool_file.txt";
	$python_binary = "/bin/python3";
	
	# Form validation and awesome start!
	if($_SERVER['REQUEST_METHOD'] == 'POST' && !empty($_POST['start']))
	{
		$ips = trim(htmlspecialchars($_POST['ips']));

		if(!empty($ips)) {
 		   $ret = file_put_contents($search_pool_file, $_POST['ips'] , LOCK_EX);
 		   if($ret === false) {
  		      die('Error writing to the file');
 		   }
 		   
			// Start the python script to get the required data
			$cmd = "cd $python_script ; $python_binary -u dimofinf.py > logs.txt &";
			shell_exec($cmd);

			# Live tail for the output
			$handle = popen("cd $python_script ; sh tail.sh", 'r');

			while(!feof($handle)) {
	      $buffer = fgets($handle);
         echo "$buffer<br/>\n";
         ob_flush();
         flush();
         }
         pclose($handle);

}
  		   else {
		       echo "<div align='left' style='color:#CE3934'><strong> Please enter IPs pool. </strong></div><br/>";
		   }
}