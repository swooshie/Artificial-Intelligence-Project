### Project

### Aditya Jhaveri - N13689134 - aaj6301

### DATA ETL Pipeline (etl.ipynb)

- Webdataset of video lectures is locally downloaded in the form of tar (youtube_dataset.tar)
- This dataset is then extracted and important details about the video (title, id) as well as subtitles files and video bytes are gathered
- Subtitles are extracted from the vtt files according to the timestamps
- Video frames are then saved to MongoDB if the caption is not matching from the previous one
- These mongodb documents contain each detail about the video frame and video it belongs to which will then be used in the next step

### Featurization and Output Pipline (featurizarion.ipynb)

- Qdrant is used to create collection to maintain feature vectors and find similar ones using cosine similarity
- Initialize OpenCLIP model for finetuning of image features using the 'openai' pretrained weights
- Initialize BERT model and tokenizer for text features
- Spacy is used for semantic chunking
- The video frames from MongoDB are converted to feature vectors and then all of these points with neccessary details in the payloads are then upserted to the qdrant's collection
- Now a list of queries is made to test the functionalities
- Sementic embedding of the respective queries is done with the same model and then nearest feature vector is found
- From this vector the appropriate video_id can be extracted which can then be used to point to the video from which the frame was clipped
- Using the minimum and maximum timestamps to clip the original video extracted form webdataset using original video id in video fram document
- Additionally captions from the mongodb dataset are extracted whose timestamp comes between min and max timestamps and whose video_id is equal to the original video id extracted from the closest point in qdrant
- Then after saving the files and subtities, they are also displayed in the notebook, subtitles are not printed cause of length log issues

Hence, the project is concluded. Thank you.