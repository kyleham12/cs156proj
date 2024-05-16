# Music_Recommender_System

# Requirements: Please install all necessary dependencies in the dependencies.txt file
+ pip install spotipy
+ pip3 install jupyter
+ pip install -U nltk
+ pip install scikit-learn
+ pip install -U flask-cors
+ npm install (make sure you have Node.js)

# Running website
+ Clone the GitHub project if not provided code files 
+ Open Model_Training.ipynb and use jupyter notebook to run all commands in it to get the df.pkl, similarity.pkl, and svc.pkl files
+ Once all pkl files are created run python app.py
+ (Optional) Getting the latest GitHub Front-end:
  + cd client
  + npm run build
  + cd ..
  + python app.py 
+ Errors:
  + If you get ValueError: X has 19298 features, but SVC is expecting #(a number) features as input. then change line 16 to num_of_features = #
  + If the list of recommended songs is taking more than 2 minutes to load then refresh the page and try again (Usually happened the first time with new pkl files)
