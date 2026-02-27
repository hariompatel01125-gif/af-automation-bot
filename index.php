<?php
// Increase time for the 12-minute process
set_time_limit(1000);
ignore_user_abort(true);

$botToken = "8377621786:AAGXu6_8ZNwDpWaTTzvbLZYz4LFoYKQw2UA";
$website = "https://api.telegram.org/bot" . $botToken;

$content = file_get_contents("php://input");
$update = json_decode($content, true);

if (!$update) {
    echo "Bot is running...";
    exit;
}

$chatId = $update["message"]["chat"]["id"];
$message = $update["message"]["text"];

if (filter_var($message, FILTER_VALIDATE_URL)) {
    $url_parts = parse_url($message);
    parse_str($url_parts['query'] ?? '', $params);
    $clickid = $params['clickid'] ?? '';

    if (empty($clickid)) {
        file_get_contents($website . "/sendMessage?chat_id=$chatId&text=" . urlencode("❌ ClickID not found!"));
        exit;
    }

    file_get_contents($website . "/sendMessage?chat_id=$chatId&text=" . urlencode("✅ Starting 12-min process for ClickID: $clickid"));

    // Step 1: Wait 4 min then send ClickID
    sleep(240);
    hitSite($clickid, "");
    file_get_contents($website . "/sendMessage?chat_id=$chatId&text=" . urlencode("🔔 Step 1 Done"));

    // Step 2: Wait 4 min then Goal 1
    sleep(240);
    hitSite($clickid, "ds_purchase_success_screen_load");
    file_get_contents($website . "/sendMessage?chat_id=$chatId&text=" . urlencode("🔔 Step 2 Done"));

    // Step 3: Wait 4 min then Goal 2
    sleep(240);
    hitSite($clickid, "dg_purchase_success_screen_load");
    file_get_contents($website . "/sendMessage?chat_id=$chatId&text=" . urlencode("🏁 Process Finished!"));

}

function hitSite($id, $goal) {
    $target = "http://akshit-bro.in/adcounty.php?i=2";
    $ch = curl_init($target);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query(['clickid' => $id, 'goal' => $goal]));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_exec($ch);
    curl_close($ch);
}
