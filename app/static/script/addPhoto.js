const imgInputHelper = document.getElementById("add-single-img");
const imgInputHelperLabel = document.getElementById("add-img-label");
const imgContainer = document.querySelector(".custom__image-container");
const imgFiles = [];

const addImgHandler = () => {
    const file = imgInputHelper.files[0];
    if (!file) return;
    // Generate img preview
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
        const newImg = document.createElement("img");
        newImg.src = reader.result;
        newImg.style = "max-width: 200px;max-height: 200px;min-width: 50px;min-height: 50px;border-radius: 500px;";
        imgContainer.insertBefore(newImg, imgInputHelperLabel);
    };
    // Store img file
    imgFiles.push(file);
    // Reset image input
    imgInputHelperLabel.style.display = "none";
    return;
};
imgInputHelper.addEventListener("change", addImgHandler);