
document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent form submission
    
    const formData = new FormData(this);
    const resultDiv = document.getElementById("result");

    resultDiv.textContent = "Processing...";

    try {
        const response = await fetch('/convert', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob();
            const downloadUrl = URL.createObjectURL(blob);

            // Create a download link
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = "converted-file";
            a.textContent = "Download Converted File";
            a.style.display = 'block';

            resultDiv.textContent = "";
            resultDiv.appendChild(a);
        } else {
            resultDiv.textContent = "Error during conversion.";
        }
    } catch (error) {
        console.error(error);
        resultDiv.textContent = "An error occurred. Please try again.";
    }
});
