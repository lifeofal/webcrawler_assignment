# webcrawler_assignment

<h1> About </h1>

Webcrawler using scrapy, bs4, numpy, matplotlib and nltk packages.

This was for my 2021 Information retrieval class. The goal was to create a spider that goes through 1000 pages in the domain of 'Kennesaw.edu'. I used the starting spider module and implemented my own scraping methods to yield back a dict of title, pageid, body, and emails.

Using bs4 I parsed the body and separated the text into one huge string literal.
After all information was 'scraped', I extracted the available links in the current page and made a recursive function to call back another parse method for the new page.


