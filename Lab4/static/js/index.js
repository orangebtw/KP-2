console.log("Hello")

const dropZone = document.getElementById("image_drop_zone")
const dropZoneBg = document.getElementById("image_drop_zone_bg")
const imageInput = document.getElementById("image")

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    const fileItems = ([...e.dataTransfer.items].filter((item) => item.kind === "file"));
    if (fileItems.length > 0) {
        if (fileItems.some((item) => item.type.startsWith("image/"))) {
            e.dataTransfer.dropEffect = "copy";
        } else {
            e.dataTransfer.dropEffect = "none";
        }
    }
});

function displayImage(files) {
    const file = files[0];
    if (file) {
        const fileURL = URL.createObjectURL(files[0]);
        dropZoneBg.style.backgroundImage = `url('${fileURL}')`;
    } else {
        dropZoneBg.style.backgroundImage = "none";
    }
}

function dropHandler(event) {
    event.preventDefault() 
    const files = [...event.dataTransfer.items]
    .map((item) => item.getAsFile())
    .filter((file) => file);
    displayImage(files);
}

dropZone.addEventListener("drop", dropHandler);
imageInput.addEventListener("change", (event) => {
    const files = event.target.files;
    displayImage(files)
});
