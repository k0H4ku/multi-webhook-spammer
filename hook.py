import requests
import os.path
import os
import time

def hook():
	try:
		if os.path.exists('./hooks.txt') == True:
			if os.stat("hooks.txt").st_size == 0:
				print("\nNo hooks found. Please add Webhook URLs to the hooks.txt file.")
			else:
				content = input('Enter what the webhook(s) should send: ')
				while True:
					for line in open('hooks.txt'):
						line = line.strip()
						req = requests.post(
							line,
							json = {
								"content": content
							}
						)
						statusCode = str(req.status_code) # Thank you Python for not allowing me to use req.status_code directly
						if statusCode.startswith('2') == True:
							print('[' + str(req.status_code) + ']' + ' Message successfully sent.')
						elif statusCode.startswith('4') == True:
							if statusCode == '429':
								retry = int(req.headers['retry-after']) / int(1000)
								print('\nGetting ratelimited. Retrying in ' + str(retry) + ' seconds.\n')
								time.sleep(retry)
							else:
								print('[' + str(req.status_code) + ']' + ' Message not sent.')
		elif os.path.exists('./hooks.txt') == False:
			print('\nNo hooks.txt file found. Please create a hooks.txt file and add webhook URLs to it.')
	except KeyboardInterrupt:
		print('\nExiting...')
		exit()

hook()