import React from "react";
import axios from 'axios';

function SearchBar() {
    return (
        <input id="searchInput" placeholder="keywords"/>
    )
}

function SearchButton() {
    // function callSearchApi(query) {
    //     return sdk.searchGet({},{
    //         q: query
    //     }, {});
    // }




    function handleClick() {
        const searched_words = document.createElement("div");
        searched_words.textContent = "Your search is:";

        const keyword = document.getElementById('searchInput').value;
        const keyword_elt = document.createElement("div");
        keyword_elt.textContent = keyword;

        const keywords_div = document.getElementById('keywords');
        keywords_div.appendChild(searched_words);
        keywords_div.appendChild(keyword_elt);

// // // using SDK

//         callSearchApi(keyword)
//             .then((response) => {
//                 console.log(response);
//             })
//             .catch((error) => {
//                 console.log(error);
//             });
//             // }

//         // var sdk = apigClientFactory.newClient({
//         //     apiKey: 'cnAVhcbgK05bIo5N0SPt31XreCtHz0tS6pXlRTrF'
//         // });


// // using Axios and API calls

        // send query to API Gateway
        const search_api = 'https://baqkofguu7.execute-api.us-east-1.amazonaws.com/prod/GET/search/';
        // const url = search_api + keyword
        // const data = {"Search": keyword};

        let reqInstance = axios.create({
            headers: {
                'x-api-key': 'cnAVhcbgK05bIo5N0SPt31XreCtHz0tS6pXlRTrF',
                "Content-Type": "application/json",
                Authorization: 'cnAVhcbgK05bIo5N0SPt31XreCtHz0tS6pXlRTrF'
            }
        })
        // const headers = {
        //     'x-api-key': 'cnAVhcbgK05bIo5N0SPt31XreCtHz0tS6pXlRTrF',
        //     "Content-Type": "application/json",
        //     Authorization: 'cnAVhcbgK05bIo5N0SPt31XreCtHz0tS6pXlRTrF'
        // }

        reqInstance
            // .post(api, data)
            .get(url)
            .then((response) => {
                console.log(response);
            })
            .catch((error) => {
                console.log(error);
            });
        // }
        // render() {
        //     return (
        //         <div>Medium Tutorial</div>
        //     );
        // }

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
            <SearchBar /><SearchButton />
            <div id="keywords"></div>
            <div>
              <br></br>
            </div>
            {/* <div id="results">Below are related pictures!</div> */}
        </div>
    );
}

export default Search;