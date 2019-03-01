import discord
import sys
from io import StringIO

TOKEN = ''

client = discord.Client()

def exec_code(code):
	#Setup streams to catch output and error
	output = StringIO()
	error = StringIO()

	sys.stdout = output
	sys.stderr = error

	exec(code)

	#restore normal stdout, stderr
	sys.stdout = sys.__stdout__
	sys.stderr = sys.__stderr__

	#retrieve the output
	o = output.getvalue()
	e = error.getvalue()
	output.close()
	error.close()

	return o,e

@client.event
async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return

	if message.content.startswith('!run'):
		msg = message.content[4:]
		if('```python' in message.content):
			msg = message.content[message.content.find('```python')+9:-3]
			out,err = exec_code(msg)
			msg = ""
			if(msg): msg += "Output: \n{}\n".format(out) 
			if(err): msg += "Error: \n{}\n".format(err) 
	await client.send_message(message.channel, msg)

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

client.run(TOKEN)
