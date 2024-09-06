function call_to_ai(input, message) {
    const mainDiv = document.getElementById("message-section");
    let userDiv = document.createElement("div");
    userDiv.id = "popup";
    userDiv.classList.add("message");
    userDiv.innerHTML = `<span id="user-response">Generating...</span>`;
    mainDiv.appendChild(userDiv);
    var scroll = document.getElementById("message-section");
    scroll.scrollTop = scroll.scrollHeight;

    // Load the Excel file and parse it
    const url = '/static/aws_inventory_detailed.xlsx';
    fetch(url)
        .then(response => response.arrayBuffer())
        .then(data => {
            const workbook = XLSX.read(data, { type: 'array' });
            const firstSheetName = workbook.SheetNames[0];
            const worksheet = XLSX.utils.sheet_to_json(workbook.Sheets[firstSheetName], { header: 1 });
            
            // Process the worksheet data and find relevant information
            let responseText = processExcelData(worksheet, message);
            userDiv.remove();
            addChat(input, responseText);
        })
        .catch(error => {
            console.error('Error reading the Excel file:', error);
            userDiv.remove();
            addChat(input, "Unfortunately, I can't access the data at the moment. Please try again later.");
        });
}

function processExcelData(worksheet, message) {
    // Process the Excel data based on the user's query
    // Here you can implement your logic to search for specific information in the worksheet
    // For simplicity, let's assume you want to search for a specific S3 bucket name

    let responseText = "Sorry, I couldn't find any relevant information.";

    for (let row of worksheet) {
        // Example: Searching for an S3 bucket in the data
        if (row.includes("S3") || row.includes("bucket")) {
            responseText = `Found an S3 bucket: ${row.join(", ")}`;
            break;
        }
    }

    return responseText;
}
