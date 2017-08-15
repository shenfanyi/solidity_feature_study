# solidity_feature_study

***the project includes:***

1,crawl the solidity code from outer web pages and create a database

2,create a text search function and provide a web API to connect

***1,solidity database***

 - multi_processing.py: main program 
 - spider.py: create 3 spider functions
 - db_manager.py: look and manage mongoDB


***2,search API***

flask.py: open server

usage: curl http://ip:port/search_content

example: curl http://10.8.47.33:5000/wallet


**return:** 

 - whole solidity code document containing the search_content 
 - receiving empty [] if no corresponding document are found


**note:** 

 - search_content is case insensitive 
 - support a-key & multi-key search

