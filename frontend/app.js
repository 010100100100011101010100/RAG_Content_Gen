// Add an event listener to the remix button
document.getElementById("remixButton").addEventListener("click", processContent());

function processContent() {
    const text = document.getElementById("contentInput").value;

    if (!text) {
        alert("Please enter some content.");
        return;
    }

    console.log("Sending data:", text);  // Log data to check if function is called

    fetch('http://127.0.0.1:5000/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Received data:", data);  // Log server response
        document.getElementById("output").textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
