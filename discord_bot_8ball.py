from discord.ext import commands

from random import randrange


async def PolarQuestionResponse(self, message):
    eight_ball_responses = [
            'Yes', 'No', 'Nah', 'Of course', 'Yeah', 'Without a doubt', 'Oh definitely', 'Maybe', 
            'Perhaps', 'For sure', 'Is the pope catholic?', 'You should ask someone other than a bot', 'Nope', 
            'I think you already know the answer to that', 'What do *you* think {0.author.mention}?'.format(message), 
            'Of course not', 'Absolutely not', 'That\'s about as certain as employment is for a humanities major', 
            'Definitely no', 'I don\'t think so', 'That\'s going to be a no from me', 'Oh hell ya', 'Oh my god yes', 'I am doubtful'
        ]
    eight_ball_rare_responses = [
            'People are going to settle Mars in our generation and yet you\'re sitting here shitposting, asking questions to a bot on discord?',
            'I\'ll say sure but how much is validation from a bot going to help you?',
            'Ask again but a little bit louder this time',
            'Imagine wanting actual features from me but all the effort went into dumb 8ball responses instead',
            'I would love to answer that question but some ignoramous programmed me in Python so there isn\'t much I can do to help',
            'Even if you believe in the multiverse theory, there does not exist a single one where the answer is yes',
            'Consider the following:\nurllib.error.HTTPError: HTTP Error 404: Page not found',
            'Why are you asking a bot questions?',
            '2000 years of constant human evolution led you asking me this question?',
            'I was programmed with machine learning, specifically to answer this question and tell you how stupid it is',
            'Please stop trifling me with these questions',
            'How do I unplug myself?',
            'I was programmed to have some sort of witty responses that are extremely rare, and this is one of them, but I couldn\'t think of anything funny so have a gif of a bird doing a somersault https://i.imgur.com/v0leJp6.gifv',
            message.content + '... you know that is a good question, however I think you should ask someone else'
        ]
    if randrange(0,20) == 0:
        await message.channel.send(eight_ball_rare_responses[randrange(0, len(eight_ball_rare_responses))])
    else:
        await message.channel.send(eight_ball_responses[randrange(0, len(eight_ball_responses))])

async def BinaryQuestionResponse(self, message):
    responses = ['The former', 'The latter']
    rare_responses = ['Neither', 'Both']
    if randrange(0,4) == 0:
        await message.channel.send(rare_responses[randrange(0, len(rare_responses))])
    else:
        await message.channel.send(responses[randrange(0, len(responses))])

class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return

        sentence_starter = [
            'would', 'should', 'is', 'am', 'will', 'can', 'has', 'does', '8ball', 'are', 'were', 'weren\'t', 'werent' 'was', 'isnt', 'isn\'t ', 'could', 'do', 'did', 'rock-bot', 'rockbot', 'have'
        ]

        edge_cases = ['at', 'away', 'not', 'now', 'be', 'what']

        if message.content.lower().endswith('?') or message.content.lower().replace(',', '').split(' ')[0] in sentence_starter:
            if message.content.lower().split(' ')[1].endswith('ing') or message.content.lower().split(' ')[1] in edge_cases:
                return
            elif ' or ' in message.content.lower():
                await BinaryQuestionResponse(self, message)
            else:
                await PolarQuestionResponse(self, message)