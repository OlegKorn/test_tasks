I'm not sure if it really checks ALL nested links of a site, but looks legit because it checks thousands of nested urls like /about, /news etc  
To iterate thru all the urls of a site in Postman you must create two requests in a collection:  

> [!TIP]
> #### Initialization ```GET {{start_url}}```[^1]
Put this code in the tab "Test" of this request:    
```
// set environment variables to default values  
postman.setEnvironmentVariable('links', '[]');  
postman.setEnvironmentVariable('url', postman.getEnvironmentVariable('start_url')); 
postman.setEnvironmentVariable('index', -1);
```
  
> [!TIP]
> #### Check urls ```GET {{url}}```
Put this code in the tab "Test" of this request:    
```
// https://blog.postman.com/check-for-broken-links-on-your-website-using-a-postman-collection/

// get environment variables
var start_url = postman.getEnvironmentVariable('start_url');
var root_url = postman.getEnvironmentVariable('root_url');
var links = JSON.parse(postman.getEnvironmentVariable('links'));
var url = postman.getEnvironmentVariable('url');
var index = parseInt(postman.getEnvironmentVariable('index'));

// increment index counter to access links in array to check
index = index + 1;

pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// if the current url includes the start_url, then this is an internal link and we should crawl it for more links
if (url.includes(start_url)) {
    // load the response body as HTML using cheerio, get the <a> tags
    var $ = cheerio.load(responseBody);

    $('a').each(function (index) {
        try { 
            var link = $(this).attr('href');

            // delete the ending "/" of href if any
            if (link.slice(-1) === "/") { 
                link = link.replace(/.$/, "");
            }
            if (link !== "undefined") {
                if (link !== "") {
                    if (link === "/") {
                        link = root_url;
                    } 
                    if (link !== "/") {
                        // if a link is relative
                        if (link.startsWith("/") && link.length > 1) {
                            link = start_url + link;
                        }
                    }
                }
                pm.test("Status code is 200", function () {
                    pm.response.to.have.status(200);
                });
                console.log(link);
            }   
            
            // add links to the links array if not already in there           
            // this is russian federation issues, if these are not banned in your state
            // delete facebook, twitter, linkedin conditions:
            if (
                link !== root_url &&          // let's try to exclude the root_url
                !links.includes(link) && 
                !link.includes("skype") && 
                !link.includes("mailto") &&
                !link.includes("facebook") &&
                !link.includes("twitter") &&
                !link.startsWith("#") &&
                !link.includes("linkedin")
            ) {
                links.push(link);
            }  
        } catch (e) {
            console.log(e, url, link);
        }
    });
}

// if we've gone through all the links, return early
if (links.length - 1 === index) {
    console.log('no more links to check');
    return;
}

// if link is a relative one, prepend with root_url
url = links[index];

// update environment variable values
postman.setEnvironmentVariable("links", JSON.stringify(links));
postman.setEnvironmentVariable("url", url);
postman.setEnvironmentVariable("index", index);

// continue calling the same request until all links are checked
postman.setNextRequest("Check URL");
```

This is what it did to https://vgbelinsky.ru (`{{base_url}} = https://vgbelinsky.ru`, `{{base_url}} = https://vgbelinsky.ru`).  
![alt text](https://i.ibb.co/r5Q8xxW/image.png)

## Any ideas and improvements?

[^1]: Create environment variables:  
{{base_url}}: the base url of a checked site  
{{start_url}}: an url of a site to check

