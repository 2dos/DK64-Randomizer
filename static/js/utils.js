function download_json_file(jsonData, filename) {
    /** Download the provided dictionary as a JSON file.
    
    Args:
        jsonData (Object): The object containing the data to be downloaded.
        filename (string): The name of the file to be downloaded.
    */
    // Check if the jsonData is already a string, if not convert it to a string
    const jsonString = typeof jsonData === "string" ? jsonData : JSON.stringify(jsonData, null, 4);

    // Create a Blob object representing the data as a JSON file
    const blob = new Blob([jsonString], { type: "application/json" });
    
    // Create an object URL for the Blob
    const url = window.URL.createObjectURL(blob);

    // Create a download link element
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;

    // Append the link to the document body
    document.body.appendChild(link);

    // Programmatically click the link to trigger the download
    link.click();

    // Remove the link from the document
    document.body.removeChild(link);

    // Revoke the object URL to free up memory
    window.URL.revokeObjectURL(url);
}
