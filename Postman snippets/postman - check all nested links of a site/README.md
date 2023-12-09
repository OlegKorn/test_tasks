I'm not sure if it really checks ALL nested links of a site, but looks legit    
To iterate thru all the urls of a site in Postman you must create two requests in a collection:  

> [!TIP]
> #### Initialize ```GET {{start_url}}```[^1]
Put this code in the tab "Test" of this request:    
```
postman.setEnvironmentVariable('startPageLinks', '[]');
postman.setEnvironmentVariable('allLinks', '[]');
postman.setEnvironmentVariable('index', 0);
postman.setEnvironmentVariable('url', postman.getEnvironmentVariable('start_url'));
```
  
> [!TIP]
> #### Collect URLs of start_page ```GET {{url}}```
Put this code in the tab "Test" of this request:    
```
// https://blog.postman.com/check-for-broken-links-on-your-website-using-a-postman-collection/

// get environment variables
var start_url = postman.getEnvironmentVariable('start_url');
var root_url = postman.getEnvironmentVariable('root_url');
var startPageLinks = JSON.parse(postman.getEnvironmentVariable('startPageLinks')) // [];

// load the response body as HTML using cheerio, get the <a> tags
var $ = cheerio.load(responseBody);

$('a').each(function (index) {
    try { 
        var link = $(this).attr('href');

        if (link !== "undefined" && 
            !link.includes("tel:") && 
            link !== "" &&
            link !== "/")
        {
            // if a link is relative
            if (link.startsWith("/") && link.length > 1) 
            {
                link = root_url + link;
            }
        }
        // add links to the links array if not already in there           
        if (link !== root_url &&          // let's try to exclude the root_url
            !startPageLinks.includes(link) && 
            !link.includes("skype") && 
            !link.startsWith("#") &&
            !link.includes("tel:") &&
            link !== "#" &&
            link !== "/" &&
            !link.includes("mailto") &&
            !link.includes("facebook") &&
            !link.includes("twitter") &&
            !link.includes("linkedin")) 
        {
            startPageLinks.push(link);
        }  
    } catch (e) {
        console.log(e, link);
    }
});

// update environment variable values
postman.setEnvironmentVariable("startPageLinks", JSON.stringify(startPageLinks));

// continue calling the same request until all links are checked
// postman.setNextRequest("Check URL");
```

> [!TIP]
> #### Collect all nested URLs ```GET {{url}}```
Put this code in the tab "Test" of this request:  
```
let startPageLinksToList = JSON.parse(
    postman.getEnvironmentVariable("startPageLinks").toString().split(",")
);
let index = postman.getEnvironmentVariable("index");
if (Number(index) === 0) {
    var allLinks = [...startPageLinksToList];
} else {
    var allLinks = postman.getEnvironmentVariable("allLinks").toString().split(",");
}
//let currentLink = startPageLinksToList[Number(index)];

let rootUrl = postman.getEnvironmentVariable("root_url"); 

// load the response body as HTML using cheerio, get the <a> tags
var $ = cheerio.load(responseBody);
    
$('a').each(function (index) {
    try { 
        var link = $(this).attr('href'); 

        // if a link is relative
        if (link.startsWith("/") && link.length > 1) {
            link = rootUrl + link;
            if (!allLinks.includes(link)) {
                allLinks.push(link);
                console.log("This link: ", link, " added");
            }
        } 
        else if (link.includes("https://") || link.includes("http://")) {
            if (!allLinks.includes(link)) {
                allLinks.push(link);
                console.log("This link: ", link, " added");
            } 
        } else {
            console.log("This link: ", link, " is not a link");
        }; 
    } catch (e) {
        console.log(e, link);
    }
});

if (Number(index) < startPageLinksToList.length) {
    console.log(allLinks);
    postman.setNextRequest("Collect all nested URLs");
} 

postman.setEnvironmentVariable("allLinks", JSON.stringify(allLinks));
```  
Put this code in the tab "Pre-request script" of this request:  
```
// listify the urls collected from GET "Collect URLs of start_page"
let startPageLinksToList = JSON.parse(
    postman.getEnvironmentVariable("startPageLinks").toString().split(",")
);

let index = postman.getEnvironmentVariable("index");
let url = postman.getEnvironmentVariable("url");
let currentLink = startPageLinksToList[Number(index)];
console.log("currentLink ", currentLink);

postman.setEnvironmentVariable("url", currentLink);
index = Number(index) + 1;
console.log("================");
console.log(index, currentLink);
console.log("================");

postman.setEnvironmentVariable("index", index);
```

## I'm not sure if it really checks all nested urls. Because when I try to run it my dead old notebook terminates postman. Any ideas and improvements?

[^1]: Create environment variables:  
{{base_url}}: the base url of a checked site  
{{start_url}}: an url of a site to check

