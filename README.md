# Tweet_Map_Backend

This backend was written in Python using Flask as part of the HackEmory-V Hackathon. 

The purpose of the webapp we built was to help combat online harassment. The user would input a location (e.g. Atlanta, GA), which would be converted to a set of geo coordinates using Google's geocode API, and sent as a post request to the backend. The backend pulled tweets from a 50 mile radius around that location, and processed them using a supervised learning NLP model which attempted to filter harassing tweets from the tweets it was given.

Tweets deemed 'harassing' in nature were returned to the frontend and displayed visually using the Google Maps API.

We submitted our project to the HackEmory-V Hackathon under the #HackHarassment challenge, and won.

The backend is still (and should continue to be) running at tweetmapbackend.herokuapp.com

It will respond to POST requests using the JSON format: {"latitude":"#####", "longitude":"#####"} with a list of tweets it deems harassing in nature, as well as the tweeter's screen name. Please note that the backend is usually in 'sleep' mode as it does not receive many requests, and will take up to 10-15 seconds to wake up initially.

It is our goal to eventually train the "Harassment Analysis Model" to better pick out harassing tweets, as well as reduce false positives.

Hackathon devpost: https://devpost.com/software/tweet_map_backend

<strong>Contributors:</strong>

https://github.com/Jomax100 : NLP algorithm and training model

https://github.com/apongos : Data Mining and Clustering of data

https://github.com/wadeAlexC : Backend written in Python using Flask, coordinated linking of backend and frontend as well as integration of NLP algorithm into backend code

https://github.com/coriandres : Frontend written in HTML, CSS, and native JS. Utilized Google APIS to present and send data.
