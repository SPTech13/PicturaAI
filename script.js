let fooocusApiUrl = null;

// Function to fetch Fooocus IP from the backend
async function getFooocusIp() {
    try {
        const response = await fetch('https://your-backend-url.onrender.com/get_fooocus_ip'); // Replace with actual backend URL
        const data = await response.json();

        if (data.success) {
            fooocusApiUrl = data.fooocus_ip;
            document.getElementById('output').innerText = 'Connected to Fooocus!';
        } else {
            document.getElementById('output').innerText = 'Error connecting to Fooocus.';
        }
    } catch (error) {
        document.getElementById('output').innerText = `Error fetching Fooocus IP: ${error.message}`;
    }
}

// Fetch Fooocus IP on page load
getFooocusIp();

async function submitForm() {
    const formData = new FormData();
    const roomImage = document.getElementById('roomImage').files[0];
    const prompt = document.getElementById('prompt').value;
    const preset = document.getElementById('preset').value;
    const outputDiv = document.getElementById('output');
    const resultDiv = document.getElementById('result');

    if (!roomImage) {
        alert("Please upload an image.");
        return;
    }

    if (!fooocusApiUrl) {
        alert("Fooocus is not connected. Try again later.");
        return;
    }

    formData.append('roomImage', roomImage);
    formData.append('prompt', prompt);
    formData.append('preset', preset);

    outputDiv.innerText = 'Uploading and processing image...';
    resultDiv.innerHTML = '';

    try {
        const response = await fetch(`${fooocusApiUrl}/generate`, { // Adjust the endpoint as needed
            method: 'POST',
            body: formData
        });
        const result = await response.json();

        if (result.success) {
            resultDiv.innerHTML = `<img src="data:image/png;base64,${result.image}" alt="Generated Design">`;
            outputDiv.innerText = 'Image processed successfully!';
        } else {
            outputDiv.innerText = `Processing failed: ${result.message}`;
        }
    } catch (error) {
        outputDiv.innerText = `An error occurred: ${error.message}`;
    }
}
