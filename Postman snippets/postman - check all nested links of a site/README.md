# POSTMAN INTERNAL LINKS CHECKER 
### ADD-ON TO THE [ARTICLE](https://blog.postman.com/check-for-broken-links-on-your-website-using-a-postman-collection/)

# HOW IT WORKS  
```
1. IT COLLECTS ALL (except pagination) INTERNAL LINKS FROM THE MAIN PAGE (OR A PAGE YOU SET)  
2. THEN IT ITERATES THRU EVERY LINK FROM STEP 1 AND IN ITS TURN COLLECTS ALL (except pagination) INTERNAL LINKS FROM EVERY ITERATED LINK AND CREATES A LIST OF ALL LINKS, CHECKING IF A LINK IS ALREADY IN THE LIST  
```

Example: for https://tropics-seeds.ru it checked 236 internal links, 12 of them were 404:
```
https://tropics-seeds.ru/shop/ehkzoticheskie-rastenija
https://tropics-seeds.ru/shop/ehkzoticheskie-rastenija/banany
https://tropics-seeds.ru/shop/ehkzoticheskie-rastenija/vodnye-rastenia
https://tropics-seeds.ru/shop/ehkzoticheskie-rastenija/dekorativno-listvennye
https://tropics-seeds.ru/shop/ehkzoticheskie-rastenija/kaudeksnye
https://tropics-seeds.ru/shop/ehkzoticheskie-rastenija/krasivo-cvetuschie
https://tropics-seeds.ru/shop/ehkzoticheskie-rastenija/ostrye-percy
https://tropics-seeds.ru/shop/ehkzoticheskie-rastenija/passiflory
https://tropics-seeds.ru/shop/ehkzoticheskie-rastenija/passiflory
https://tropics-seeds.ru/shop/ehkzoticheskie-rastenija/plodovye
https://tropics-seeds.ru/shop/ehkzoticheskie-rastenija/nasekomoyadnye
https://tropics-seeds.ru/shop/ehkzoticheskie-rastenija/hvoinye
```

### These 5 requests are:
--------------------------  
> [!TIP]
> #### 1. Initialize ```GET {{start_url}}```[^1]
Put this code in the tab "Tests" of this request:    
```
// https://blog.postman.com/check-for-broken-links-on-your-website-using-a-postman-collection/

postman.setEnvironmentVariable('startPageLinks', '[]');
postman.setEnvironmentVariable('allLinks', '[]');
postman.setEnvironmentVariable('index', 0);
postman.setEnvironmentVariable('url', postman.getEnvironmentVariable('start_url'));
```
--------------------------  
> [!TIP]
> #### 2. Collect URLs of start_page ```GET {{start_url}}```
Put this code in the tab "Tests" of this request:    
```
// https://www.freecodecamp.org/news/how-to-validate-urls-in-javascript/
function isValidHttpUrl(str) {
  const pattern = new RegExp(
    '^(https?:\\/\\/)?' + // protocol
      '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
      '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR ip (v4) address
      '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
      '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
      '(\\#[-a-z\\d_]*)?$', // fragment locator
    'i'
  );
  return pattern.test(str);
}


// get environment variables
var start_url = postman.getEnvironmentVariable('start_url');
var root_url = postman.getEnvironmentVariable('root_url');

var startPageLinks = JSON.parse(postman.getEnvironmentVariable('startPageLinks')); // [];
var allLinks = JSON.parse(postman.getEnvironmentVariable('allLinks')); // []

// load the response body as HTML using cheerio, get the <a> tags
var $ = cheerio.load(responseBody);

$('a').each(function (index) {
    try 
    { 
        var link = $(this).attr('href');

        if (link !== "undefined" && 
            !link.includes("tel:") && 
            link.length !== 0 &&
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
            !link.includes("javascript:") &&
            !link.startsWith("#") &&
            !link.includes("tel:") &&
            link !== "#" &&
            link !== "/" &&
            !link.includes("mailto") &&
            !link.includes("facebook") &&
            !link.includes("twitter") &&
            !link.includes("linkedin")) 
        {
            console.log(link);
            startPageLinks.push(link);
            allLinks.push(link);
        }
    } catch (e) {
        console.log(e, link);
    }
});

// update environment variable values
postman.setEnvironmentVariable("startPageLinks", JSON.stringify(startPageLinks));
```
--------------------------  
> [!TIP]
> #### 3. Collect all nested URLs ```GET {{url}}```

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
postman.setEnvironmentVariable("index", index);
```
  
Put this code in the tab "Tests" of this request:  
```
// https://www.freecodecamp.org/news/how-to-validate-urls-in-javascript/
function isValidHttpUrl(str) {
  const pattern = new RegExp(
    '^(https?:\\/\\/)?' + // protocol
      '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
      '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR ip (v4) address
      '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
      '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
      '(\\#[-a-z\\d_]*)?$', // fragment locator
    'i'
  );
  return pattern.test(str);
}

let startPageLinksToList = JSON.parse(
    postman.getEnvironmentVariable("startPageLinks").toString().split(",")
);

// let startPageLinksToListNumberToCheck = 5;

let index = postman.getEnvironmentVariable("index");

if (Number(index) === 1) {
    var allLinks = [...startPageLinksToList];
}
if (Number(index) > 1) {
    var allLinks = postman.getEnvironmentVariable("allLinks").toString().split(",");
}

let rootUrl = postman.getEnvironmentVariable("root_url"); 
let rootUrlWithoutSchema = postman.getEnvironmentVariable("rootUrlWithoutSchema");

// load the response body as HTML using cheerio, get the <a> tags
var $ = cheerio.load(responseBody);

$('a').each(function (index) {
    try { 
        var link = $(this).attr('href'); 
        // if a link is relative
        if (link.startsWith("//") && link.includes(rootUrlWithoutSchema)) {
            link = link.replace("//", "").replace(rootUrlWithoutSchema, "");
        }
        if (link.startsWith("/") && link.length > 1) {
            link = rootUrl + link;
            if (isValidHttpUrl(link) && !allLinks.includes(link)) {
                allLinks.push(link);
            }
        } 
        else if (link.includes("https://") || link.includes("http://")) {
            if (isValidHttpUrl(link) && !allLinks.includes(link)) {
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

console.log("Collect all nested URLs:", "index=", index, allLinks);

// if your PC is old and slow
// set startPageLinksToListNumberToCheck = 3 or 5 instead of startPageLinksToList.length
if (Number(index) < startPageLinksToList.length) {
    postman.setNextRequest("Collect all nested URLs");
}
```
--------------------------  
> [!TIP]
> #### 4. Set index == 0 ```GET {{url}}```
Put this code in the tab "Tests" of this request:
```
postman.setEnvironmentVariable("index", 0);
```
--------------------------  
> [!TIP]
> #### 5. Check collected URLs ```GET {{url}}```
Put this code in the tab "Pre-request script" of this request:
```
// listify the urls collected from GET "Collect all nested URLs"
let allLinks = postman.getEnvironmentVariable("allLinks").split(","); // -> []
let index = postman.getEnvironmentVariable("index");
console.log("Request: 'Check collected URLs';", "index=", index, allLinks);

let currentLink = allLinks[Number(index)];;

postman.setEnvironmentVariable("url", currentLink);

if (Number(index) < allLinks.length) {
    index = Number(index) + 1;
} 

postman.setEnvironmentVariable("index", index);
```
Put this code in the tab "Tests" of this request:
```
let allLinks = postman.getEnvironmentVariable("allLinks").split(","); // -> []
let index = postman.getEnvironmentVariable("index");

if (Number(index) < allLinks.length) {
    pm.test("Finish check of all collected site internal links: status code is 200", function () {
        pm.response.to.have.status(200);
    });

    postman.setNextRequest("Check collected URLs");
}
```

#### Seems to really catch & check all links of a site. This far it has 3 requests as a result of which there is a list of internal links of a website.

[Here](https://github.com/OlegKorn/test_tasks/blob/main/Postman%20snippets/postman%20-%20check%20all%20nested%20links%20of%20a%20site/Check%20all%20nested%20links%20of%20a%20site.postman_collection) is the postman project.  
[Here](https://github.com/OlegKorn/test_tasks/blob/main/Postman%20snippets/23%20-%20check%20all%20nested%20links%20of%20a%20site/tropics-seeds.ru%20-%20236%20internal%20links)  is the json of result - a list of 236 internal links created of tropics-seeds.ru (w/o full pagination).

Any ideas and improvements?  

[^1]: Create environment variables:  
{{base_url}}: the base url of a checked site  
{{start_url}}: an url of a site to check
{{rootUrlWithoutSchema}}: root_url w/o schema

