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
