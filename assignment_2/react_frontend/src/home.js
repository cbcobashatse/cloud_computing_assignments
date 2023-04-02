import React from "react";
import { useNavigate } from "react-router-dom";


function SearchButton() {
    const navigate = useNavigate()

    function handleClick() {
        navigate("/search_photos")
    }

    return (
        <button onClick={handleClick}>
            Search
        </button>
    );
}

function UploadButton() {
    const navigate = useNavigate()
    
    function handleClick() {
        navigate("/upload_photos")
    }

    return (
        <button onClick={handleClick}>
            Upload
        </button>
    );
}

const Home = () => {
  return (
    <div>
        <h1>Welcome to your photo album!</h1>
        Feel free to to do any of the following:<br/>
        - upload images to the album<br/>
        - search the album by key words using text or speech<br/>
        <br/>
        <SearchButton /><UploadButton />
    </div>
  );
};

export default Home;
