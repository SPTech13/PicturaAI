async function submitForm() {
    const formData = new FormData();
    const roomImage = document.getElementById('roomImage').files[0];
    if (!roomImage) {
        alert("Please upload an image.");
        return;
    }

    formData.append('roomImage', roomImage);

    try {
        const response = await fetch('https://your-backend-url.onrender.com/process.php', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();

        if (result.success) {
            document.getElementById('result').innerHTML = `<img src="data:image/png;base64,${result.image}" alt="Generated Design">`;
        } else {
            document.getElementById('result').innerHTML = `<p>Error: ${result.message}</p>`;
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById('result').innerHTML = "<p>There was an error processing the request.</p>";
    }
}
