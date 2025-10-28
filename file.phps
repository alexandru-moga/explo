<?php

ini_set('display_errors', 0);
$out   = false;
$url   = $_POST['url'] ?? false;
$error = false;
$links = [];

// if ($url && !preg_match('#^https?://([a-z0-9-]+\.)*[a-z0-9-]+\.[a-z0-9-]+/.+#i', $url)) {
//     $error = 'Invalid URL';
// } else if ($url && preg_match('/\.(htaccess|ph(p\d?|t|tml))$/i', $url)) {
//     $error = 'Sneaky you!';
// }

if (!$error && $url) {
    $unique = uniqid() . bin2hex(openssl_random_pseudo_bytes(8));
    $target = 'uploads/' . $unique;
    mkdir($target, 0777, true);
    chdir($target);
    touch('.htaccess');

    // Vulnerable extraction
    $cmd = "curl -sk '$url' | tar --no-overwrite-dir --no-same-owner --no-same-permissions -xf - 2>&1";
    $out = "\$ cd $target" . PHP_EOL;
    $out .= '$ ' . $cmd . PHP_EOL;
    $out .= shell_exec($cmd);

    // Attempt to clean up php-based extensions
    $cmd = "bash -c 'rm $target/*.{php,pht,phtml,php4,php5,php6,php7}'";
    $out .= '$ ' . $cmd . PHP_EOL;
    $out .= shell_exec($cmd) . PHP_EOL;

    // Build file list
    $files = array_diff(scandir("."), ['.', '..', '.htaccess']);
    foreach ($files as $file) {
        if (is_file($file)) {
            $safeFile = htmlspecialchars($file, ENT_QUOTES);
            $links[] = "<a href=\"uploads/$unique/$safeFile\" target=\"_blank\">$safeFile</a>";
        }
    }
}

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Archiver</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .container {
            margin-top: 80px;
        }
        .card {
            border: none;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        .card-header {
            font-size: 1.2rem;
            font-weight: bold;
            background-color: #0d6efd;
            color: white;
            border-top-left-radius: 16px;
            border-top-right-radius: 16px;
        }
        .form-control {
            border-radius: 10px;
        }
        .btn {
            border-radius: 10px;
        }
        pre {
            background-color: #f1f1f1;
            padding: 20px;
            border-radius: 10px;
            overflow-x: auto;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>

<div class="container">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <h2 class="text-center mb-4">🚀 Secure File Management of Arhive</h2>
            <div class="card">
                <div class="card-header">
                    Provide a URL to fetch and extract
                </div>
                <form class="p-4" method="POST">
                    <?php if ($error): ?>
                        <div class="alert alert-danger"><?php echo htmlentities($error); ?></div>
                    <?php endif; ?>
                    <div class="mb-3">
                        <label for="url" class="form-label">URL to download:</label>
                        <input type="text" id="url" name="url" placeholder="https://example.com/archive.tar" value="<?php echo htmlentities($url ?? '', ENT_QUOTES); ?>" class="form-control" required>
                    </div>
                    <button type="submit" class="btn btn-primary float-end">Download</button>
                </form>

                <?php if ($out): ?>
                    <div class="border-top px-4 py-3 bg-light">
                        <h6 class="mb-2">Output:</h6>
                        <pre><code><?php echo htmlentities($out); ?></code></pre>
                    </div>
                <?php endif; ?>

            </div>
        </div>
    </div>
</div>

</body>
</html>
