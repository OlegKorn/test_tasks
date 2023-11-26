- [x] \### _Работоспособность: Проверьте, выполняются ли запросы и получаемые ответы корректны. Определите любые ошибки, неожиданные статусы или отсутствующие данные._

Выполнено рекурсивных (т.е. все ссылки сайта) тестов в Postman (статус запроса 200, время отзыва более 15 секунд), т.е. являются ли ссылки работающими:

  #### crezu-fifth.finclic.com - 490
  ![crezu-fifth.finclic.com](https://raw.githubusercontent.com/OlegKorn/test_tasks/main/crezu-fifth.finclic.com/postman/postman%20main%20page%20490%20tests.JPG)
  
  #### crezu.es - 10811
  ![crezu.es](https://raw.githubusercontent.com/OlegKorn/test_tasks/main/crezu-fifth.finclic.com/postman/crezu.es%2010811%20tests.JPG)
  
  #### crezu.mx - 2026, 19 провалено
  ![crezu.es](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/crezu.mx%202026%20%20tests%2019%20failed.JPG)
  ![crezu.es](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/crezu.mx%20failed1.JPG)
  ![crezu.es](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/crezu.mx%20failed2.JPG)
  ![crezu.es](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/crezu.mx%20failed3.JPG)
  ![crezu.es](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/crezu.mx%20failed4.JPG)
  
  #### crezu.co - 369, 3 провалено
  ![crezu.co](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/crezu.co%20369%20tests%203%20failed.JPG)
  ![crezu.co](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/crezu.co%20failed1.JPG)
  
  #### crezu.pe - 495, 7 провалено
  ![crezu.pe](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/crezu.pe%20495%20tests%207f.JPG)
  ![crezu.pe](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/crezu.pe%20failed1.JPG)
  ![crezu.pe](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/crezu.pe%20failed2.JPG)
  
  #### crezu.ro - 5002, 3 провалено
  ![crezu.ro](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/crezu.ro%205002%20tests%203f.JPG)
  ![crezu.ro](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/crezu.ro%20failed.JPG)
  
  #### crezu.pl - 18441, 1 провален
  ![crezu.pl](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/crezu.pl%2018411%20tests%201f.JPG)
  ![crezu.pl](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/crezu.pl%20failed.JPG)
  
  #### crezu.kz - 7387, 3 провалено
  ![crezu.kz](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/crezu.kz%207387%20tests%203f.JPG)
  ![crezu.kz](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/crezu.kz%20failed.JPG)
  
  #### crezu.vn - 321
  ![crezu.vn](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/crezu.vn%20321%20tests.JPG)
  
  #### crezu.lk - 822
  ![crezu.lk](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/crezu.lk%20822%20%20tests.JPG)

  #### 2 ссылки с https://crezu-fifth.finclic.com/reg/#! (https://crezu-fifth.finclic.com/terms.pdf и https://crezu-fifth.finclic.com/privacy-policy.pdf) выдают ошибку 404:
   ![crezu-fifth.finclic.com/reg/#!](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/404%20terms%20pdf.JPG)
   ![crezu-fifth.finclic.com/reg/#!](https://github.com/OlegKorn/test_tasks/blob/main/crezu-fifth.finclic.com/postman/404%20privacy%20policy%20pds.JPG)


  ## Функциональность: Проверьте работоспособность всех интерактивных элементов, таких как кнопки, формы, выпадающие списки и т. д. Обратите внимание на любые ошибки или неожиданное поведение.

  ### BUGS:
  ## video 1
  1. Go to https://crezu-fifth.finclic.com/
  2. Click "Allow" of popup "Allow notifications"
  3. Click "Request your loan"
  4. At the page https://crezu-fifth.finclic.com/reg/#! the popup appears again
  
  ER: After step 2 cookies must be set and the popup must not appear again
  
  AR: The popup appears again on step 4
  
  ## video 2
  1. Go to https://crezu-fifth.finclic.com/
  2. Click "Allow" of popup "Allow notifications"
  3. Click "Request your loan"
  4. At the page https://crezu-fifth.finclic.com/reg/#! fill required inputs with valid data
  5. Click "Request your loan"
  
  ER: After step 5 a user must be navigated to the next page
  
  AR: A popup appears: "Hold on We are looking for the best offer for you.
  Please don't close this page. Reviewed lenders: 1 logo Loan Application Fill out the form and get money", then nothig happens due to errors:

  ```
  Запрос из постороннего источника заблокирован: Политика одного источника запрещает чтение удаленного ресурса
  на https://test.crezu.net/form/v2. (Причина: не удалось выполнить запрос CORS). Код состояния: (null).

  sendGroupToBackend error Error: Network Error
    gm https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:787
    onerror https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:788
    r https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:22
    pt https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:9
    crezu_reg_form https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:22
    crezu_reg_form https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:22
    ty https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:13
    crezu_reg_form https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:788
    _m https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:788
    LC https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:788
    request https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:788
    t https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:788
    crezu_reg_form https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:787
    sendDataToBackend https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:791
    crezu_reg_form https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:5
    sendGroupByNameToBackend https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:791
    crezu_reg_form https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:5
    processActiveGroup https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:791
    crezu_reg_form https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:5
    activateNextGroup https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:791
    crezu_reg_form https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:5
    y https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:792
    Nn https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    Ft https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    $g https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    r https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:792
    Nn https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    Ft https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    n https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    r https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:22
    Yb https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:22
    sy https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:13
    Yv https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    Jv https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    t_ https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    x https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    m https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    g https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    j https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    run https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    update https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    A https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    T https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    N https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    g https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    E https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    I https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    g https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    E https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    x https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    m https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    g https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    j https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    run https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    update https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    A https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    T https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    N https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    g https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
    j https://cdn.staging.crezu.net/reg_form/dist/crezu_reg_form.iife.js:1
  ```

  ## video 3
  1. Go to https://crezu-fifth.finclic.com/
  2. Click "Request your loan"
  3. At the page https://crezu-fifth.finclic.com/reg/#! click browser back arrow

  ER: The page navigates to https://crezu-fifth.finclic.com/

  AR: The page stays on https://crezu-fifth.finclic.com/reg/#!, an error happens on clicking the back arrow:
  ```
  Некоторые куки неправильно используют рекомендованный атрибут «SameSite» 
  Для куки «_fbp» не установлено корректное значение атрибута «SameSite». Вскоре куки без атрибута «SameSite» или с некорректным значением этого атрибута будут рассматриваться как «Lax». Это означает, что куки больше не будут отправляться в сторонних контекстах. Если ваше приложение зависит от доступности этих кук в подобных контекстах, добавьте к ним атрибут «SameSite=None». Чтобы узнать больше об атрибуте «SameSite», прочитайте https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie/SameSite fbevents.js:24:97002
  Для куки «_fbp» не установлено корректное значение атрибута «SameSite». Вскоре куки без атрибута «SameSite» или с некорректным значением этого атрибута будут рассматриваться как «Lax». Это означает, что куки больше не будут отправляться в сторонних контекстах. Если ваше приложение зависит от доступности этих кук в подобных контекстах, добавьте к ним атрибут «SameSite=None». Чтобы узнать больше об атрибуте «SameSite», прочитайте https://developer.mozilla.org/docs/Web/HTTP/Headers/Set-Cookie/SameSite
  ```

  ## video 4
  1. Go to https://crezu-fifth.finclic.com/
  2. Scroll down to the "What can you use a microloan for?" section
  3. Click any of "Choose ->" carousel buttons

  ER: The user is navigated to the loan page

  AR: Nothing happens, maybe the error is in the button event code where "o" is passed instead of 0:
  ```
  https://crezu-fifth.finclic.com/_nuxt/1b22668.modern.js

  function(t) {
    if (t.target === t.currentTarget || t.timeStamp >= o || t.timeStamp <= 0 || t.target.ownerDocument !== document)
        return c.apply(this, arguments)
  }
  ```

  ## video 5
  1. Go to https://crezu-fifth.finclic.com
  2. Scroll down to the comment section
  3. Fill the name input (placeholder "Your name"), and the comment input (placeholder "Write your comment here..."), set "Rate us"
  4. Click "Submit"

  ER: A comment must be posted

  AR: The "name" input only receives digits


  ## error 6: visual
  1. Go to https://crezu-fifth.finclic.com
  2. Scroll down to the comment section

  ER: There are title and comment text inputs. They must have right placeholders for each, respectively

  AR: The comment input has placeholder "Your name", and the name input has it "Write your comment here..."


  ## error 7: content (video 6)
  1. Go to https://crezu-fifth.finclic.com
  2. Scroll down to the comment section
  3. Click at the arrows of the input "Write your comment here...

  ER: Comments input must not have controls for setting digits as its value

  AR: The given input has contrils for setting digits as its value


  
  ## error 8: functional (video 7)
  1. Go to https://crezu-fifth.finclic.com
  2. Scroll down to the comment section
  3. Input a non-digital value in the input "Write your comment here...
  4. Click "Submit"
  5. Click the red cross icon appeared at the right corner of the input

  ER: The red cross icon appeared at the right corner of the input must clear its value

  AR: The red cross icon appeared at the right corner of the input does not clear its value


  ## error 9: functional (video 8)
  1. Go to https://crezu-fifth.finclic.com
  2. Scroll down to the "What can you use a microloan for?" section
  3. Click left slider arrow 5-6 times, then the right one till the content doesnot move

  ER: These arrows must get inactive since the content does not move more

  AR: The slider arrows are still active even if the content does not move more


  ## bug 10: security JS (video 9)
   1. Go to https://crezu-fifth.finclic.com
  2. Scroll down to the comment section
  3. Input a digital value in the input "Write your comment here...
  4. Input:
  ```"<object src=1 href=1 onerror="javascript:alert("Amicus libertae ego sum)"></object>"```
  or
  ```"<script charset="\x22>javascript:alert(1)</script>"```
  or
  ```<a href="\x11javascript:javascript:alert(1)" id="fuzzelement1">test</a>```
  or
  ```"'><img src=xxx:x \x00onerror=javascript:alert(1)>```
  to the "Your name" input
  6. Click "Submit"

  ER: JS-scripts must not run via injections

  AR: JS alert popup "1" with OK button appears


  ## functional bug 11: (video 10)
  1. Go to https://crezu-fifth.finclic.com
  2. Scroll down to the comment section
  3. Click laft arrow of the comments so that the content does not move

  ER: These arrows must get inactive since the content does not move more

  AR: These arrows are active even if the content does not move more


  
