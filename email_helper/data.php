<?php
if (isset($_COOKIE["super_secret_cookie"]) && $_COOKIE["super_secret_cookie"] === "LinuxNetwork2022"
    && isset($_POST['username']) && isset($_POST["homework_name"])) {
    //all iis nice
} else {
    header('Location:index.php');
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1" name="viewport"/>
    <meta content="" name="description"/>
    <title>LinuxNetwork 2022 progress check site</title>
    <link href="https://uneex.ru/favicon.ico" rel="shortcut icon"/>
    <!--Frameworks-->
    <link href="https://timetable.veniamin.space/css/bootstrap.css" rel="stylesheet"/>
    <script crossorigin="anonymous" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM"
            src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <!--General ccs, js-->
    <link href="https://timetable.veniamin.space/css/night_mode.css" rel="stylesheet"/>
    <script src="https://timetable.veniamin.space/js/night_mode.js"></script>
    <style>
        html {
            height: 100vh;
        }

        body {
            min-height: 100vh;
            max-height: 100vh;
            max-width: 100vw;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-bottom: 5rem;
        }

        .form-control-general {
            max-width: 90%;
            margin: auto;
        }

        @media screen and (max-width: 800px) {
            .form-control-general {
                max-width: 100%;
                margin: auto;
            }
        }

        .my_fit {
            height: 80vh;
        !important;
        }
    </style>
</head>
<body class="">
<div class="text-center form-control-general">
    <h1 class="h3 mb-3 fw-normal">LinuxNetwork2022 User Progress Check</h1>
    <?php
    echo "
    <div>
        <h5>Username is: ".$_POST['username']."</h5>
        <h5>Current task name is: ".$_POST['homework_name']."</h5>
    </div>
    "
    ?>
    <div class="overflow-scroll my_fit">
        <table class="table table-hover table-striped table-bordered align-middle" id="main_table">
            <thead>
            <tr>
                <th scope="col">№</th>
                <th scope="col">Input</th>
                <th scope="col">Output</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <th>1</th>
                <th>lol</th>
                <th>kek</th>
            </tr>
            <tr>
                <th>1</th>
                <th>lol</th>
                <th>kek</th>
            </tr>
            <tr>
                <th>1</th>
                <th>lol</th>
                <th>kek</th>
            </tr>
            <tr>
                <th>1</th>
                <th>lol</th>
                <th>kek</th>
            </tr>
            </tbody>
        </table>
    </div>
</div>
<footer class="bg-transparent fixed-bottom-right">
    <div class="container-fluid">
        <a class="btn btn-danger btn-lg night-button m-2 fs-6">Night Mode</a>
    </div>
</footer>
</body>
</html>
