<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_FILES['roomImage'])) {
        $image = $_FILES['roomImage'];

        // Get API key from environment variable
        $api_key = getenv('FOOOCUS_API_KEY');

        // Convert image to base64
        $base64Image = base64_encode(file_get_contents($image['tmp_name']));

        // Prepare payload for the API
        $payload = json_encode([
            'image' => $base64Image,
            'furnish_options' => [
                'kitchen' => ['item' => 'cabinet', 'color' => '#ffffff'],
                'bathroom' => ['item' => 'sink', 'color' => '#ffffff'],
                'livingRoom' => ['item' => 'sofa', 'color' => '#ffffff']
            ]
        ]);

        // Initialize cURL request to Fooocus API
        $ch = curl_init('https://fooocus-api-url/v1/generate');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Authorization: ' . 'Bearer ' . $api_key
        ]);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);

        // Execute cURL request
        $response = curl_exec($ch);
        curl_close($ch);

        if ($response) {
            $responseData = json_decode($response, true);
            if (isset($responseData['image'])) {
                echo json_encode(['success' => true, 'image' => $responseData['image']]);
            } else {
                echo json_encode(['success' => false, 'message' => 'Image generation failed.']);
            }
        } else {
            echo json_encode(['success' => false, 'message' => 'API request failed.']);
        }
    } else {
        echo json_encode(['success' => false, 'message' => 'No image uploaded.']);
    }
} else {
    echo json_encode(['success' => false, 'message' => 'Invalid request method.']);
}
?>
