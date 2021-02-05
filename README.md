# Twitter/Facebook Awareness Bot

This is an awareness bot made for COVID-19 support/relief efforts, but by changing the key word, ex. "covid-19", in every file, this can be an awareness bot for any topic given the training data. The programs parse tweets from Twitter, then post the link and a screenshot of the Tweet to Facebook (given a Facebook developer account, and a page to post the data).

## Initialization
To start, run gettrainingdata.py. This parses the Twitter database for all tweets relating to the keyword. From there, it is the user's job to manually sort the training data into good and bad categories.

```bash
python gettrainingdata.py
```

## Running
To run the awareness bot, you run trainingandtesting.py, then awarenessbot.py.
Running trainingandtesting.py is to train the bag-of-words model, grab the most recent keyword data from Twitter, and run it against the model.
```bash
python trainingandtesting.py
```
Running awarenessbot.py has multiple steps. First, a screenshot is taken in HTML format of the tweet that was determined to be a good tweet. Then, the HTML received is converted into an image, and saved. Finally, the URL to the tweet and the image are posted to the designated Facebook page.
```bash
python awarenessbot.py
```

Created in Summer of 2020
