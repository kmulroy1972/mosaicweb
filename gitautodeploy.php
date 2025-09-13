<?php
// Cloudways Git Auto Deploy webhook endpoint for GitHub
// - Verifies GitHub HMAC signature (X-Hub-Signature-256)
// - Matches branch and triggers Cloudways Git Pull via API
//
// Configure via environment variables (recommended) or query params:
//   CLOUDWAYS_EMAIL, CLOUDWAYS_API_KEY, CLOUDWAYS_SERVER_ID, CLOUDWAYS_APP_ID,
//   CLOUDWAYS_BRANCH, CLOUDWAYS_GIT_URL (optional), GITHUB_WEBHOOK_SECRET
// Query param overrides (use judiciously):
//   ?server_id=...&app_id=...&branch_name=...&git_url=...
//
// GitHub webhook: set Content type = application/json and provide the same secret.

declare(strict_types=1);

// Lightweight config loader: supports config.php and .env alongside env vars
function load_local_config(): array {
    $cfg = [];
    // 1) config.php returns an associative array
    $configPhp = __DIR__ . '/config.php';
    if (is_file($configPhp)) {
        $data = include $configPhp;
        if (is_array($data)) {
            $cfg = array_merge($cfg, $data);
        }
    }
    // 2) .env simple KEY=VALUE parser (no quotes or escapes)
    $envPath = __DIR__ . '/.env';
    if (is_file($envPath)) {
        $lines = @file($envPath, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) ?: [];
        foreach ($lines as $line) {
            $line = trim($line);
            if ($line === '' || $line[0] === '#') continue;
            $pos = strpos($line, '=');
            if ($pos === false) continue;
            $k = trim(substr($line, 0, $pos));
            $v = trim(substr($line, $pos + 1));
            if ($k !== '') {
                $cfg[$k] = $v;
            }
        }
    }
    return $cfg;
}

$localCfg = load_local_config();

// Basic JSON response helper
function respond(int $code, array $data): void {
    http_response_code($code);
    header('Content-Type: application/json');
    echo json_encode($data);
    exit;
}

// Read raw payload
$payload = file_get_contents('php://input');
if ($payload === false) {
    respond(400, ['ok' => false, 'error' => 'Unable to read request body']);
}

// GitHub event validation
$event = $_SERVER['HTTP_X_GITHUB_EVENT'] ?? '';
if ($event !== 'push') {
    respond(202, ['ok' => true, 'message' => 'Ignoring non-push event', 'event' => $event]);
}

// Retrieve secret for HMAC verification
$secret = $localCfg['GITHUB_WEBHOOK_SECRET'] ?? (getenv('GITHUB_WEBHOOK_SECRET') ?: '');
if (isset($_GET['secret'])) { // last-resort override; avoid if possible
    $secret = (string)$_GET['secret'];
}
if ($secret === '') {
    respond(500, ['ok' => false, 'error' => 'Missing webhook secret configuration']);
}

// Validate HMAC signature (sha256)
$sigHeader = $_SERVER['HTTP_X_HUB_SIGNATURE_256'] ?? '';
if (!preg_match('/^sha256=([a-f0-9]{64})$/', $sigHeader, $m)) {
    respond(401, ['ok' => false, 'error' => 'Missing or invalid signature header']);
}
$signature = $m[1];
$computed = hash_hmac('sha256', $payload, $secret);
if (!hash_equals($computed, $signature)) {
    respond(401, ['ok' => false, 'error' => 'Signature verification failed']);
}

// Parse JSON body
$data = json_decode($payload, true);
if (!is_array($data)) {
    respond(400, ['ok' => false, 'error' => 'Invalid JSON payload']);
}

// Determine branch from webhook
$ref = $data['ref'] ?? '';
// Expect format: refs/heads/<branch> (avoid PHP 8-only str_starts_with for compat)
$pushedBranch = '';
if ($ref !== '' && strpos($ref, 'refs/heads/') === 0) {
    $pushedBranch = substr($ref, strlen('refs/heads/'));
}

// Effective config (env first, then query overrides)
$serverId = isset($_GET['server_id']) ? (string)$_GET['server_id'] : ($localCfg['CLOUDWAYS_SERVER_ID'] ?? (getenv('CLOUDWAYS_SERVER_ID') ?: ''));
$appId    = isset($_GET['app_id'])    ? (string)$_GET['app_id']    : ($localCfg['CLOUDWAYS_APP_ID']  ?? (getenv('CLOUDWAYS_APP_ID')  ?: ''));
$branch   = isset($_GET['branch_name']) ? (string)$_GET['branch_name'] : ($localCfg['CLOUDWAYS_BRANCH'] ?? (getenv('CLOUDWAYS_BRANCH') ?: ''));
$gitUrl   = isset($_GET['git_url'])   ? (string)$_GET['git_url']   : ($localCfg['CLOUDWAYS_GIT_URL'] ?? (getenv('CLOUDWAYS_GIT_URL') ?: ''));

if ($branch === '' && $pushedBranch !== '') {
    $branch = $pushedBranch;
}

if ($serverId === '' || $appId === '' || $branch === '') {
    respond(500, [
        'ok' => false,
        'error' => 'Missing required Cloudways configuration (server_id, app_id, branch_name)'
    ]);
}

// Only act for matching branch
if ($pushedBranch !== '' && strcasecmp($pushedBranch, $branch) !== 0) {
    respond(202, [
        'ok' => true,
        'message' => 'Push to different branch; skipping deploy',
        'pushed' => $pushedBranch,
        'target' => $branch,
    ]);
}

// Cloudways credentials
$cwEmail = $localCfg['CLOUDWAYS_EMAIL']   ?? (getenv('CLOUDWAYS_EMAIL')   ?: '');
$cwKey   = $localCfg['CLOUDWAYS_API_KEY'] ?? (getenv('CLOUDWAYS_API_KEY') ?: '');
if ($cwEmail === '' || $cwKey === '') {
    respond(500, ['ok' => false, 'error' => 'Missing Cloudways API credentials']);
}

// cURL helper
function curl_json(string $url, array $payload, array $headers = [], int $timeout = 25): array {
    $ch = curl_init($url);
    if ($ch === false) {
        return ['ok' => false, 'error' => 'Failed to init curl'];
    }
    $body = http_build_query($payload);
    $defaultHeaders = ['Content-Type: application/x-www-form-urlencoded'];
    $allHeaders = array_merge($defaultHeaders, $headers);
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $body,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CONNECTTIMEOUT => 10,
        CURLOPT_TIMEOUT => $timeout,
        CURLOPT_HTTPHEADER => $allHeaders,
    ]);
    $resp = curl_exec($ch);
    $http = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $err  = curl_error($ch);
    curl_close($ch);
    if ($resp === false) {
        return ['ok' => false, 'status' => $http, 'error' => $err ?: 'Request failed'];
    }
    $json = json_decode($resp, true);
    if (!is_array($json)) {
        return ['ok' => false, 'status' => $http, 'error' => 'Non-JSON response', 'raw' => $resp];
    }
    return ['ok' => ($http >= 200 && $http < 300), 'status' => $http, 'json' => $json];
}

// 1) Obtain Cloudways access token
$tokenResp = curl_json(
    'https://api.cloudways.com/api/v1/oauth/access_token',
    [
        'email'  => $cwEmail,
        'api_key'=> $cwKey,
    ]
);
if (!$tokenResp['ok']) {
    respond(502, ['ok' => false, 'stage' => 'token', 'error' => $tokenResp['error'] ?? 'Token request failed']);
}
$accessToken = $tokenResp['json']['access_token'] ?? '';
if ($accessToken === '') {
    respond(502, ['ok' => false, 'stage' => 'token', 'error' => 'Missing access_token in response']);
}

// 2) Trigger Git Pull on Cloudways
$pullPayload = [
    'server_id'   => $serverId,
    'app_id'      => $appId,
    'branch_name' => $branch,
];
// Some setups require git_url in pull; include if provided
if ($gitUrl !== '') {
    $pullPayload['git_url'] = $gitUrl;
}

$pullResp = curl_json(
    'https://api.cloudways.com/api/v1/git/pull',
    $pullPayload,
    ['Authorization: Bearer ' . $accessToken],
    60
);

if (!$pullResp['ok']) {
    respond(502, [
        'ok' => false,
        'stage' => 'pull',
        'status' => $pullResp['status'] ?? 0,
        'error' => $pullResp['error'] ?? 'Pull request failed',
        'response' => $pullResp['json'] ?? ($pullResp['raw'] ?? null),
    ]);
}

respond(200, [
    'ok' => true,
    'message' => 'Deployment triggered',
    'branch' => $branch,
    'cloudways' => $pullResp['json'] ?? null,
]);
