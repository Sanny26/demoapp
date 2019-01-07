Title: Collections Report 9
Slug: collections-report-9
Category: Collections Project
Date: 2019-01-08
Modified: 2019-01-08
Authors: Santhoshini Gongidi

# Work Done:
- Studied different online demo systems to redesign the UI for Focused Collections project.
- Redesigned the UI for Focused collections project. 

------

## Links

Link to Focused Collections Project: [Click here]()

## Focused Collections Project

Online Demo applications used to study and redesign the UI for the project are:

- [Visual Search of BBC News](http://www.robots.ox.ac.uk/~vgg/research/on-the-fly/)
- [Text Search of BBC News](http://www.robots.ox.ac.uk/~vgg/research/text/index.html)
- [Oxford Buildings search](http://www.robots.ox.ac.uk/~vgg/research/oxbuildings/index.html)
- [Demos for different models](https://www.clarifai.com/demo)


#### Other details about the portal:
Required storage space for a collection:

| Files                     | Size                 |
|---------------------------|----------------------|
| HWNet Model               | 620 MB               |
| KDTree for Retrieval      | 515 MB               |
| Word Position Information | 4 MB                 |
| Blog documents and words  | 300 MB (37000 words) |

HWNet model size is independent of the collection. The size of other files is dependent on the number of words in a collection.

The total processing for a given query to generate results is 17.19 seconds. If we run the model on system having >10GB memory, the processing time will be reduced even further. Due to insufficient memory available to load and process that entire model in real time, smaller chunks are loaded to process the query.

The site has been designed such that the admin can add new collections using a form and providing the above required files to process a query.

-----
# Work to be done:
- Make changes to the focused collections project based on the reviews received.
- Plan to work on word recognition models built by Kartik. As we plan to build a demo system for word recognition as well, I would like to test out these models and move the project code to pytorch.
