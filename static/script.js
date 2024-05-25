document.querySelector("#uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData();
    const imageInput = document.querySelector("#imageInput");

    if (imageInput.files.length === 0) {
        alert("Please upload an image file.");
        return;
    }

    formData.append("image", imageInput.files[0]);

    const loadingIndicator = document.querySelector("#loadingIndicator");
    loadingIndicator.classList.remove("hidden");

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error);
        }

        const data = await response.json();


        loadingIndicator.classList.add("hidden");

        const uploadedImage = document.querySelector("#uploadedImage");
        uploadedImage.src = URL.createObjectURL(imageInput.files[0]);

        const description = document.querySelector("#description");
        description.innerHTML = data.description.replace(/\n/g, "<br>");

        const extractedTextDiv = document.querySelector("#extractedText");
        extractedTextDiv.innerHTML = data.extracted_text.replace(/\n/g, "<br>");

        const segmentedImage = document.querySelector("#segmentedImage");
        segmentedImage.src = data.segmented_image + '?' + new Date().getTime();

        const results = document.querySelector("#results");
        results.classList.remove("hidden");
    } catch (error) {
        alert("Error: " + error.message);
        loadingIndicator.classList.add("hidden");
    }
});



document.querySelector("#imageInput").addEventListener("change", function (e) {
    const imageInput = e.target;

    if (imageInput.files.length === 0) {
        return;
    }

    const reader = new FileReader();

    reader.onload = function (event) {
        // Display the image
        const uploadedImage = document.querySelector("#uploadedImage");
        uploadedImage.src = event.target.result;

        const uploadedPhotoWrapper = document.querySelector(".uploaded-photo-wrapper");
        uploadedPhotoWrapper.classList.remove("hidden");

        const results = document.querySelector("#results");
        results.classList.add("hidden");
    };

    reader.readAsDataURL(imageInput.files[0]);
});