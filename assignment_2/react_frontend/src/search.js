import React from "react";
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMicrophone } from '@fortawesome/free-solid-svg-icons';

function reInitialize() {
    const keywords_div = document.getElementById('keywords');
    while(keywords_div.firstChild) {
        keywords_div.removeChild(keywords_div.firstChild);
    }
    const results_div = document.getElementById('results');
    while(results_div.firstChild) {
        results_div.removeChild(results_div.firstChild);
    }
}

function DisplayResults(results) {
    const your_results = document.createElement("div");
    if (results.length == 0){
        your_results.textContent = "No images were found!";
        const results_div = document.getElementById('results');
        results_div.appendChild(your_results);
    }
    else{
        your_results.textContent = "Below are images found!";
        const results_div = document.getElementById('results');
        results_div.appendChild(your_results);

        console.log(results)

        let i;
        for(i=0; i < results.length; i++){
            const image_data = results[i]
            const image_link = "https://" + image_data.bucket + ".s3.us-east-1.amazonaws.com/" + image_data.objectKey
            console.log(image_link)

            const image = document.createElement('img');
            image.src = image_link;
            results_div.appendChild(image);
        }
    }
}

function HandleSearch(searchString) {
    const searched_words = document.createElement("div");
    searched_words.textContent = "Your search is:";

    const keyword_elt = document.createElement("div");
    keyword_elt.textContent = searchString;

    const keywords_div = document.getElementById('keywords');
    keywords_div.appendChild(searched_words);
    keywords_div.appendChild(keyword_elt);

    // send query to API Gateway
    const search_api = 'https://baqkofguu7.execute-api.us-east-1.amazonaws.com/prod/search';
    const headers = {
        'x-api-key': 'cnAVhcbgK05bIo5N0SPt31XreCtHz0tS6pXlRTrF'
    };
    const queryStringParams = {
        'q': searchString
    };

    axios
        .get(search_api, {params: queryStringParams, headers: headers})
        .then((response) => {
            const results = response.data
            DisplayResults(results);
        })
        .catch((error) => {
            console.log(error);
        });
}

function handleMicrophone() {
    reInitialize()
    const keyword = document.getElementById('searchInput')
    keyword.value = ""
    console.log("starting speech recognition")

    // code adapted from https://tutorialzine.com/2017/08/converting-from-speech-to-text-with-javascript
    try {
        // const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        // const SpeechRecognition = window.speechRecognition || window.webkitSpeechRecognition;
        // const SpeechRecognition = window.webkitSpeechRecognition;
        // const recognition = new SpeechRecognition.SpeechRecognition();
        const recognition = new window.webkitSpeechRecognition();
        recognition.onstart = function() { 
            console.log('Voice recognition activated. Try speaking into the microphone.')
        }
        recognition.onspeechend = function() {
            console.log('You were quiet for a while so voice recognition turned itself off.')
        }
        recognition.onerror = function(event) {
            if(event.error == 'no-speech') {
                console.log('No speech was detected. Try again.')
            };
        }
        recognition.onresult = function(event) {
            // event is a SpeechRecognitionEvent object.
            // It holds all the lines we have captured so far. 
            // We only need the current one.
            const current = event.resultIndex;
            console.log("current")
            console.log(current)
            
            // Get a transcript of what was said.
            const searchString = event.results[current][0].transcript;
            console.log("search string")
            console.log(searchString)
            
            // perform the search on the searched word
            const keyword = document.getElementById('searchInput')
            keyword.value = searchString
            HandleSearch(searchString)
        }
        console.log("starting recognition")
        recognition.start();
        console.log("recognition done")
      }
      catch(e) {
        console.error(e);
      }
}

function SearchBar() {
    return (
        <input id="searchInput" placeholder="keywords"/>
    )
}

function SearchButton() {
    function handleClick() {
        reInitialize()
        const keyword = document.getElementById('searchInput').value;
        HandleSearch(keyword)
    }
    return (
            <button onClick={handleClick}>
                Search Keywords
            </button>
    );
}

function Search() {
    return (
        <div>
            <h1>Welcome to your photo album!</h1>
            Search the album by key words using text or speech<br/>
            <br/>
            <SearchBar />
            <SearchButton />
            <br></br>
            <br></br>
            Make your search by voice!{'    '}
            <FontAwesomeIcon icon={faMicrophone} id="microphone" onClick={handleMicrophone}/>
            <br></br>
            <br></br>
            <div id="keywords"></div>
            <div>
              <br></br>
            </div>
            <div id="results"></div>
        </div>
    );
}

export default Search;