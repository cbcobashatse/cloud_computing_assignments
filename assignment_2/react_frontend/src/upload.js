import React, { useState } from "react";
import axios from 'axios';


function FileUpload() {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileInputChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = () => {
    // Code to upload the selected file
    const customLabels = document.getElementById("customLabels").innerHTML
    console.log(selectedFile);
    console.log(customLabels);
    const fileName = selectedFile.name
    // const fileName_components = fileName.split('.')
    // fileName = fileName_components[0]
    const fileSize = '' + selectedFile.size
    const fileType = selectedFile.type
    console.log(fileName)
    console.log(fileSize)
    console.log(fileType)


    // send POST query to API Gateway
    const upload_api = 'https://baqkofguu7.execute-api.us-east-1.amazonaws.com/prod/upload/' + fileName;
    const headers = {
        'x-api-key': 'cnAVhcbgK05bIo5N0SPt31XreCtHz0tS6pXlRTrF',
        'x-amz-meta-customLabels': customLabels,
        'Content-Type': fileType
    };

    axios
      .put(upload_api, selectedFile, {headers: headers})
      .then(function(response) {
            if (response.status === 200) {
                const labels_div = document.getElementById('labels');
                while(labels_div.firstChild) {
                    labels_div.removeChild(labels_div.firstChild);
                }
                const file_div = document.getElementById('file');
                while(file_div.firstChild) {
                    file_div.removeChild(file_div.firstChild);
                }
    
                const upload_response = document.createElement("div");
                upload_response.textContent = "Photo successfully uploaded";
          
                const upload_response_div = document.getElementById('upload_response');
                upload_response_div.appendChild(upload_response);
                console.log("Photo successfully uploaded")
            }

      })
      .catch((error) => {
          console.log(error);
      });



  };

  return (
    <div>
      <input type="file" id="file" onChange={handleFileInputChange} />
      <br/>
      <br/>
      <Label /><SpecifyLabel />
      <div id="labels"></div>
      <br/>
      <br/>
      <button onClick={handleFileUpload}>Upload Photo</button>
      <div id="upload_response"></div>
    </div>
  );
}


function Label() {
    return (
        <input id="labelInput" placeholder="Label"/>
    )
}

function SpecifyLabel() {
    const [labels, setLabels] = useState([]);
    function handleClick() {
      const specified_label = document.createElement("div");
      specified_label.textContent = "Labels specified are:";

      const label = document.getElementById('labelInput').value;
      const newLabels = [...labels, label]
      setLabels(newLabels);
      const label_elt = document.createElement("div");
      label_elt.setAttribute("id", "customLabels");
      label_elt.textContent = newLabels;

      const labels_div = document.getElementById('labels');
      while(labels_div.firstChild) {
          labels_div.removeChild(labels_div.firstChild);
      }
      labels_div.appendChild(specified_label);
      labels_div.appendChild(label_elt);

      console.log(newLabels)
      const label_input = document.getElementById('labelInput');
      label_input.value = ""
    }

    return (
        <button onClick={handleClick}>
            Specify Label
        </button>
    );
}

function Upload() {
    return (

        <div>
            <h1>Welcome to your photo album!</h1>
            Upload a photo to your album!<br/>
            <br/>
            <FileUpload />
        </div>
    );
}

export default Upload;