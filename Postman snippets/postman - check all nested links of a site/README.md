# HOW IT WORKS  
```
1. IT COLLECTS ALL INTERNAL LINKS FROM THE MAIN PAGE (OR A PAGE YOU SET)  
2. THEN IT ITERATES THRU EVERY LINK FROM STEP 1 AND IN ITS TURN COLLECTS ALL INTERNAL LINKS FROM EVERY ITERATED LINK AND CREATES A LIST OF ALL LINKS CHECKING IF A LINK IS ALREADY IN THE LIST  
```

## I'm not sure if it really checks ALL internal links of a site, but looks legit. Maybe it does not collect pagination. 
To iterate thru all the urls of a site in Postman you must create four requests in a collection (there are 3 now, giving out a list of website links). The last one I was too lazy to write. You can do it yourself - just create the 4th request and pass there the list of links from the 3rd request, and for each do your tests.  

I cant collect all links for a site (e.g. I tried `worldbirds.ru`, its main page has 63 links, but my notebook is dead and terminates the full cycle so I only did 5 links).

### These 3 requests are:

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
> #### Collect URLs of start_page ```GET {{start_url}}```
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
```

> [!TIP]
> #### Collect all nested URLs ```GET {{url}}```
Put this code in the tab "Test" of this request:  
```
let startPageLinksToList = JSON.parse(
    postman.getEnvironmentVariable("startPageLinks").toString().split(",")
);

let index = postman.getEnvironmentVariable("index");

if (Number(index) === 1) {
    var allLinks = [...startPageLinksToList];
}
if (Number(index) > 1) {
    var allLinks = postman.getEnvironmentVariable("allLinks").toString().split(",");
}

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
                console.log("This link is added: ", link);
                allLinks.push(link);
            }
        } 
        else if (link.includes("https://") || link.includes("http://")) {
            if (!allLinks.includes(link)) {
                console.log("This link is added: ", link);
                allLinks.push(link);
            } 
        } else {
            return;
        }; 
        postman.setEnvironmentVariable("allLinks", allLinks);
    } catch (e) {
        console.log(e, link);
    }
});

if (Number(index) < 5) {
    postman.setNextRequest("Collect all nested URLs");
    //console.log(allLinks);
} 

console.log(allLinks);
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

postman.setEnvironmentVariable("url", currentLink);
index = Number(index) + 1;
console.log("================");
console.log(index, currentLink);
console.log("================");

postman.setEnvironmentVariable("index", index);
```

#### Seems to really catch & check all links of a site. This far it has 3 requests as a result of which there is a list of internal links of a website.

[Here](https://github.com/OlegKorn/test_tasks/blob/main/Postman%20snippets/postman%20-%20check%20all%20nested%20links%20of%20a%20site/Check%20all%20nested%20links%20of%20a%20site.postman_collection/) is the postman project.    
[Here](https://github.com/OlegKorn/test_tasks/blob/main/Postman%20snippets/postman%20-%20check%20all%20nested%20links%20of%20a%20site/result%20-%20%205%20first%20links%20-%20worldbirds.ru/) is the json of result - a list of some 90 links created by the first 5 internal links of wordbirds.ru.  

Any ideas and improvements?  

[^1]: Create environment variables:  
{{base_url}}: the base url of a checked site  
{{start_url}}: an url of a site to check

