// code copied from https://stackoverflow.com/questions/46119987/upload-and-read-a-file-in-react
class FileInput extends React.Component {
    // function FileInput() {
        constructor(props) {
          super(props)
          this.uploadFile = this.uploadFile.bind(this);
        }
        
        uploadFile(event) {
            let file = event.target.files[0];
            // const [files, setFiles] = this.setState([file])
            // this.setState()
            this.setState({files:[file]})
            console.log(file);
            
            if (file) {
              let data = new FormData();
              data.append('file', file);
              console.log(data)
              // axios.post('/files', data)...
            }
        }
        
        render() {
          return <span>
            <input type="file"
            name="myFile"
            id="fileInput"
            onChange={this.uploadFile} />
          </span>
        }
    }
    




    function SpecifyLabel() {
      const [labels, setLabels] = useState([]);
      function handleClick() {
        const specified_label = document.createElement("div");
        specified_label.textContent = "Labels specified are:";
  
        const label = document.getElementById('labelInput').value;
        const label_elt = document.createElement("div");
        label_elt.textContent = label;
  
        const labels_div = document.getElementById('labels');
      //   console.log("previously")
      //   console.log(labels_div.value)
        labels_div.appendChild(specified_label);
        labels_div.appendChild(label_elt);
  
        // add label to labels state
        // this.setLabels(labels.concat(label))
        // this.setState({files:[file]})
        // setLabels({labels: labels['labels'].push(label)})
        // var previousLabels = labels['labels']
        console.log('previous')
        console.log(labels)
        const newLabels = [...labels, label]
        // var newLabels = previousLabels.push(label)
  
        // setLabels({labels: previousLabels.push(label)})
        setLabels(newLabels);
        // setLabels({labels:[label]})
        // setLabels(labels.push(label))
      //   this.setState({labels: this.state.labels.concat([label])})
      //   this.state.labels = this.state.labels.concat([label])
        console.log("current")
        console.log(newLabels)
        // console.log(previousState)
  
        // figure out formatting of the specified labels
        // const keywords = keyword_elt.toString().split(',');
        // console.log(keyword_elt)
      }
  
      return (
          <button onClick={handleClick}>
              Specify Label
          </button>
      );
  }


  import React, { useState } from "react";
import axios from 'axios';


function UploadPhoto() {
    function HandleClick() {
        console.log("Photo Uploaded")
        const file = document.getElementById('fileInput');
        // const file = useState([files])
        // const file = {files}
        // const file = this.state.files
        console.log(file)
        // navigate("/search_photos")

        // set the HTTP request and POST the photo to the S3 bucket
    }

    return (
        <button onClick={HandleClick}>
            Upload Photo
        </button>
    );
}

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
    const fileSize = '' + selectedFile.size
    const fileType = selectedFile.type//.substring(6)
    console.log(fileName)
    console.log(fileSize)
    console.log(fileType)


    // send POST query to API Gateway
    const upload_api = 'https://baqkofguu7.execute-api.us-east-1.amazonaws.com/prod/upload/' + fileName;
    const headers = {
        'x-api-key': 'cnAVhcbgK05bIo5N0SPt31XreCtHz0tS6pXlRTrF',
        'x-amz-meta-customLabels': customLabels,
        // 'Content-Length': fileSize,
        'Content-Type': fileType
    };

    axios
      .put(upload_api, selectedFile, {headers: headers})
      .then((response) => {
          // const results = response.data
          console.log(response)
          // displayResults(results);
      })
      .catch((error) => {
          console.log(error);
      });



  };

  return (
    <div>
      <input type="file" onChange={handleFileInputChange} />
      <br/>
      <br/>
      <Label /><SpecifyLabel />
      <div id="labels"></div>
      <br/>
      <br/>
      {/* <UploadPhoto onClick={handleFileUpload} /> */}
      <button onClick={handleFileUpload}>Upload Photo</button>
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

      // figure out formatting of the specified labels
      // const keywords = keyword_elt.toString().split(',');
      // console.log(keyword_elt)
    }

    return (
        <button onClick={handleClick}>
            Specify Label
        </button>
    );
}

function Upload() {
    const [labels, setLabels] = useState([])
    // const [files, setFiles] = useState([])

    // const labels = list()

    return (

        <div>
            <h1>Welcome to your photo album!</h1>
            Upload a photo to your album!<br/>
            <br/>
            {/* <FileInput /> */}
            <FileUpload />
            {/* <br/>
            <br/>
            <Label /><SpecifyLabel />
            <div id="labels"></div>
            <br/>
            <br/>
            <UploadPhoto /> */}
        </div>
    );
}

export default Upload;