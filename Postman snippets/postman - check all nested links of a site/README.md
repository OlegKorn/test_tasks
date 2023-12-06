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

pm.test("Status code is 200", function() {
    pm.response.to.have.status(200);
});
pm.test("Response time is below 15000ms", function() {
    pm.expect(pm.response.responseTime).to.be.below(15000);  
});

// if the current url includes the start_url, then this is an internal link and we should crawl it for more links
// if (url.includes(start_url)) {
if (url.includes(start_url)) {
    // load the response body as HTML using cheerio, get the <a> tags
    var $ = cheerio.load(responseBody);
    
    $('a').each(function (index) {
        var link = $(this).attr('href');

        // if a link is relative
        if (link.startsWith("/")) {
            link = start_url + $(this).attr('href').replace("http:/", "");
            pm.test("Status code is 200", function () {
                pm.response.to.have.status(200);
            });
        } else if (/^https?:\/\//.test(link)) {
            pm.test("Status code is 200", function () {
                pm.response.to.have.status(200);
            });
        }

        // add links to the links array if not already in there
        // if you have additional links you would like to exclude, for example, ads, you can add this criteria as well

        // this is russian federation issues, if these are not banned in your state
        // delete this if:
        if ( 
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
    });
}

// if we've gone through all the links, return early
if (links.length - 1 === index) {
    console.log('no more links to check');
    return;
}

// if link is a relative one, prepend with root_url
url = links[index];

if (! /^https?:\/\//.test(url)) {
    url = root_url + url;
} else {
    url = url;
}

// update environment variable values
postman.setEnvironmentVariable("links", JSON.stringify(links));
postman.setEnvironmentVariable("url", url);
postman.setEnvironmentVariable("index", index);

// continue calling the same request until all links are checked
postman.setNextRequest("Check URL");
```

[^1]: Create an environment variable {{start_url}} - an url of a site to check - before
