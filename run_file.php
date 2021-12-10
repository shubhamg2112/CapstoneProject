<?php
if($_SERVER['REQUEST_METHOD'] == "POST") {
    $uploadDir = 'uploads/'; 
    $uploadStatus = 1; 
    $uploadedFile = '';
    $response = array( 
        'status' => 0, 
        'message' => 'Form submission failed, please try again.' 
    );
    if(!empty($_FILES["uploaded_file"]["name"])){
        $today = date("m-d-Y_H:i:s");
        // File path config 
        $fileName = basename($_FILES["uploaded_file"]["name"]); 
        $newfilename= date('dmYHis').str_replace(" ", "", basename($_FILES["uploaded_file"]["name"]));
        $targetFilePath = $uploadDir.$newfilename; 
        $fileType = pathinfo($targetFilePath, PATHINFO_EXTENSION);

        $allowTypes = array('csv'); 
        if(in_array($fileType, $allowTypes)){ 
                    // Upload file to the server 
            if(move_uploaded_file($_FILES["uploaded_file"]["tmp_name"], $targetFilePath)){ 
                $uploadedFile = $fileName; 
                $response['message'] = 'File Uploaded';
            }else{ 
                $uploadStatus = 0; 
                $response['message'] = 'Sorry, there was an error uploading your file.'; 
            } 
        }else{ 
            $uploadStatus = 0; 
            $response['message'] = 'Sorry, only PDF, DOC, JPG, JPEG, & PNG files are allowed to upload.'; 
        }
        echo $response['message'];
    }
    if($uploadStatus == 1){   
        $op = [];
        $r = "";
        putenv("PATH=C:\Users\Shubham Gupta\AppData\Local\Programs\Python\Python39");
        $cmd_str = 'python C:/xampp/htdocs/project-python/SampleJupyter.py ' .$targetFilePath;
        //exec($cmd_str, $op, $r);
        
        ob_start();
        exec($cmd_str. " 2>&1", $op);
        $result = ob_get_contents();
        ob_end_clean();

        //echo "<pre>";
        //print_r($op);
        //echo "</pre>";

        $myfile = fopen($op[0], "r") or die("Unable to open file!");

        if ($myfile) {
            echo "<table border='1' id='table_result'>";
            while (($line = fgets($myfile)) !== false) {
                // process the line read.
                //print_r($line);
                $line_exploded = explode(",", $line);
                echo "<tr>";
                foreach($line_exploded as $val) {
                    echo "<td>".$val."</td>";
                }
                echo "</tr>";
            }
            echo "</table>";
            echo "<input type='hidden' name='dynamic_file' id='dynamic_file' value='".$op[0]."' />";
            fclose($myfile);
        } else {
            // error opening the file.
            echo "<h2>Error opening the results.</h2>";
        } 

    }
}



?>