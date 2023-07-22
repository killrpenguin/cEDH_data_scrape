# cEDH_data_scrape
My goal with this code is to create an object that I can use to scrape decklists gathered from the commander DDB
and combine them into one large pandas dataframe for further study. This repo will hold all of the files I create to 
gather, clean, organize and analyze the nearly 400 decks currently posted to the cEDH DDB.

The object will have the following attributes:
  - A random number between 10 and 30. This will slow the process down and randomize my reuqests, making it harder to
      identify my scraping.
  - A proxy server address so that I can rotate through a proxy pool to further hide my scraping.
  - A list object to store the deck list in so that I can create a txt copy of each deck list.
      This will let me check each list as I go, to confirm the quality of the data. It will also
      act as a way of tracking, incase I can't do the entire scraping at once.
  - A link pulled from a python list. This list is the target URL to be scraped.
  - This object will hold the method for scraping the data.
  - The data will go to a global pandas DF.
