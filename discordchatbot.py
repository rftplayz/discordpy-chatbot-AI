import discord
from discord.ext import commands
import wikipedia,os
from chatbot import Chat, register_call

# You can put any prefix
prefix = "the prefix that you want"

bot = commands.Bot(command_prefix = prefix)

#This code is for the AI
@register_call("whoIs")
def who_is(query, session_id="general"):
    try:
        return wikipedia.summary(query)
    except Exception:
        for new_query in wikipedia.search(query):
            try:
                return wikipedia.summary(new_query)
            except Exception:
                pass
    return "I don't know about "+query

#This code is for the file of the AI, is very important
template_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"chatbotTemplate","chatbottemplate.template")

chat=Chat(template_file_path)

#This will say you in the shell when the bot is ready. This code is optional
@bot.event
async def on_ready():
    print("Bot is ready!")

#The next code is for the bot can reply
@bot.command(pass_context = True)
async def chatbot(ctx, *, message):
    result = chat.respond(message)
    if(len(result)<=2048):
        embed=discord.Embed(title="ChatBot AI", description = result, color = (0xF48D1))
        await ctx.send(embed=embed)
    else:
        embedList = []
        n=2048
        embedList = [result[i:i+n]for i in range(0, len(result), n)]
        for num, item in enumerate(embedList, start = 1):
            if(num == 1):
                embed = discord.Embed(title="ChatBot AI", description = item, color = (0xF48D1))
                embed.set_footer(text="Page{}".format(num))
                await ctx.send(embed = embed)
            else:
                embed = discord.Embed(description = item, color = (0xF48D1))
                embed.set_footer(text = "Page {}".format(num))
                await ctx.send(embed = embed)

#Put your token here
bot.run("Your token goes here")
