# TwitterPicParser

This is a joke project that I did over summer 2021 because I was bored and lazy. You need at least python 3.7.

I retweet a lot of art on twitter, but I dislike how tedious it is to download art.
I was lazy, so I spent more time making this program then it would've to download all of the images I ever retweeted.

Yes, I know it's slow, I have several sleep() calls becuase I didn't feel like searching the selenium API for a way to wait for HTML elements that don't exist in the page yet (This doesn't even really seem possible tbh, but lmk if you have any ideas or solutions).

As of now the outputs are redirected from stdout to a file called output.txt because of buggy VSCode terminal.

How to run:

Go to directory where PicParse.py is.
python3 PicParse.py TWITTER_USERNAME NUMBER_OF_IMAGES

Some stats/issues:

- Takes roughly 8 minutes to download 1000 images. 

- Selenium seems to run out of memory at around 3000 images. Currently haven't found a solution.

Some stuff you need:


Python packages:

- Selenium (install using pip)

- Requests (also using pip)


Other stuff:

- Chromedriver (this has to match the version of your chrome brower.)

- A directory called "pictures" inside the directory with PicParse.py
