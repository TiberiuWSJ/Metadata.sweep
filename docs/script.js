async function extractMetadata() {
    const fileInput = document.getElementById("fileInput");
    const output = document.getElementById("output");
    output.textContent = "Processing...";
  
    if (fileInput.files.length === 0) {
      output.textContent = "Please select a file.";
      return;
    }
  
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
  
    try {
      const res = await fetch("https://YOUR_BACKEND_URL/extract-metadata", {
        method: "POST",
        body: formData,
      });
  
      const result = await res.json();
      output.textContent = JSON.stringify(result.metadata || result, null, 2);
    } catch (err) {
      output.textContent = "❌ Error: " + err.message;
    }
  }
  