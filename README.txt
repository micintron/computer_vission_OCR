Document and Materials AI/ML Computer Vision Processor - NLP Extension

This project will be an Extension of the original CI challenge for Computer vision and OPEN CV. Our new objectives are to gather data from new form of id - Drivers license, summarize - text extracted with BERT and OpenCV, classify text being extracted - using basic classification like Sentiment Analysis, update old angular UI in with a brand new react UI, create auto documentation with Sphinx and show template with Sphinx that can be used for any project for easy integration.

Business Value	

- Further enhanced Automated documentation processing from images

State of the Art NLP- Natural language processing for further data analysis and data classification 
New visual and tooling based data visualizations in react for ease of use and testing
Fully integrated and automated documentation tooling with Sphinx that can be integrated easily into any git project.


Deliverables	

A Python Flask based API that can take in non text based documents such as a driver license -

A React application to interact with said API for UI based tools such as the upload feature and visualize back results.

A Flask API for performing NLP on targets extracted text such as Summarization and Classification

To use Run 
docker compose build 
- then 
Docker compose up

This will build a nested container with both the ui and the API service fully up and running

Important note:
Set you docker memory to 12 GB before you run loading the AI models takes a lot 
If ui goes up but API stops on compose up try restarting the container before extending memory then if that dose not work extend memory and try to start container again 

Side Note:
The drivers_license endpoint may take a few moments running locally but host on a production server with GPU access this will run in less than a second.

Use files in test data to test application



Full Team

Suvarna, Satyanarayana (CTR)
Team Organizer

Cintron, Matthew I 
AI ML / Backend Implementation Lead

Das, Avishek 
AI ML Dev / DL data extraction

Tulluru, Laxmisudha 
AI ML Dev / DL data extraction

Watts, Robert W 
AI ML research- DL data extraction


Valle, Troy T 
Full Stack UI Lead

Dunlap, Thomas A 
AI ML / backend Implementation / NLP

Cirtain, Melissa J 
AI ML Research /  NLP

Godbehere, Andrew B
AI ML Dev / Sphinx Documentation

Omar, Mohammed A
AI ML Testing / Documentation/ Research

Niziorski, Piotr W
Endpoint Research 








