# solidity_feature_study

***the project includes:***

1,crawl the solidity code from outer web pages and create a database

2,create a text search function and provide a web API to connect

***1,solidity database***

 - multi_processing.py: main program 
 - spider.py: create 3 spider functions
 - db_manager.py: look and manage mongoDB


***2,search API***

search_API_flask.py: open server, must start mongoDB first

usage: curl ip:port/search_content

example: curl 192.168.0.101:5000/wallet， curl 127.0.0.1:5000/wallet


**return:** 

 - whole solidity code document containing the search_content 
 - receiving empty [] if no corresponding document are found


**note:** 

 - search_content is case insensitive 
 - support a-key & multi-key search

