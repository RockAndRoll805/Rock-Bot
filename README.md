# Rock-Bot 

Rockbot is a discord bot I have been working on in my free time that runs off of discord.py.

Its features are pretty random and mostly are spontaneously created to fulfill wants and needs of myself or friends in my Discord server.

## Features:

### 8 ball
Rockbot will try to analyze sentences to see if someone is asking a binary question (yes or no question) and then give a random response. When rockbot gives a response, there is a 1/20 chance for him to give a rare response which might be something snarky or humorous. The feature is not perfect right now but I have ideas of how to make it not reply to false positives in the future; one of which being to use natural language toolkit.

### Animals
Pics of animals, on demand. Includes foxes, shibes, dogs, cats, and birds.

### Bash Shell
Using Python's subprocess library Rockbot can execute system commands in Discord and output the response in chat. This command only works if the user trying to execute a command matches my user ID.

### Dice
Roll any amount of any die of any size.

### Dictionary
Get the definition any of a word using Merriam-Webster's API. There is also code to try to parse Urbandictionary for definitions, however UD has no APIs so it is all done through web scraping. The UD feature currently does not work in all cases but there is not much need for this feature so it might be a bit before it gets updated.

### Lyrics
Parses what the user types, searches for the song, and then outputs a link to genius.com.

### Maintenance
Allows only me to terminate or restart rockbot from a chat command.

### Math
Evaluates message for math operations and performs them using various Python math libraries.

### Purge
Mass remove messages from the channel this command is invoked. Only moderators can use this command.

### Steam
Allows users to add links to their Steam profiles. Then they can ask what they should play on Steam, to which rockbot responds with a random game.

### Stocks
Creates and posts a graph of the value of any ticker from the past day.

### Timer
Create reminders for a certain date or within a certain time of reminder creation time. Reminders can be for the user who created it, another user in the server, or a server role. When the reminder time has been reached, the user or role is pinged with the contents of the original reminder text.

### Voice
This is a music feature that allows users to search for songs and add them to a queue. This feature uses YoutubeDL for song downloading and can download anything from its supported links.

### Wargroove
Various commands relating to the game of Wargroove. One command outputs prins in chat a grid that visualizes range on a square based grid. Another is for calculating probability of lethal. The math calculations have some errors when calculating high ends of bell curve but it works outside of that. I would like to get around to fixing the math errors.
