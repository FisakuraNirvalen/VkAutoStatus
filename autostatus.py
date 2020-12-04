import vk_api
import datetime
import colorama
from colorama import Fore
colorama.init()

editnumber = [('0', '0⃣'), ('1', '1⃣'), ('2', '2⃣'), ('3', '3⃣'), ('4', '4⃣'), ('5', '5⃣'), ('6', '6⃣'), ('7', '7⃣'), ('8', '8⃣'), ('9', '9⃣')]
ballnumber = [('0', ''), ('1', '❶'), ('2', '❷'), ('3', '❸'), ('4', '❹'), ('5', '❺'), ('6', '❻'), ('7', '❼'), ('8', '❽'), ('9', '❾')]
holeballnumber = [('0', ''), ('1', '➀'), ('2', '➁'), ('3', '➂'), ('4', '➃'), ('5', '➄'), ('6', '➅'), ('7', '➆'), ('8', '➇'), ('9', '➈')]

class status(object):
	"""docstring for status"""
	def __init__(self, token, decor=0, debug=0, online = 0, friends = 0):
		super(status, self).__init__()
		self.decor = decor
		if token != '' and debug == 0:
			self.token = True
			self.debug = 0
		else:
			self.token = False
			self.debug = 1
		self.online = online
		self.friends = friends

		vk = vk_api.VkApi(token=token)
		self.vk = vk

		# аккаунт
		name = vk.method('account.getProfileInfo')
		self.first_name = name['first_name']
		self.last_name = name['last_name']
		self.screen_name = name['screen_name']

		# ваши подписчики
		self.followerson = len(vk.method('users.getFollowers', {'count': '1000'})["items"])
		self.friendsonline = len(vk.method('friends.getOnline'))
		self.bannedon = vk.method('account.getBanned', {'count': '200'})["count"]

		# ваши диалоги
		self.unreadmessageon = vk.method('account.getCounters', {'filter': 'messages'})['messages']

		# статистика вашего аккаунта
		self.avalikes = vk.method('photos.get', {'album_id': 'profile', 'rev': 1, 'extended': 1, 'count': 1})["items"][0]["likes"]["count"]
		self.giftscounton = vk.method('gifts.get', {'count': '200'})["count"]

		# дата и время
		t = datetime.datetime.now()
		self.time = t.strftime("%H:%M")

	
	def date(self):
		t = datetime.datetime.now()
		return f'[{Fore.CYAN}{t}{Fore.RESET}]'
	def get_status(self, title):
		if self.decor == 1:
			for old, new in editnumber:
				title = title.replace(old, new)
		if self.decor == 2:
			for old, new in ballnumber:
				title = title.replace(old, new)
		if self.decor == 3:
			for old, new in holeballnumber:
				title = title.replace(old, new)

		try:
			if (len(title)< 140):
				if self.debug == 0:
					self.vk.method("status.set", {"text": title}) #отправка запроса на установку статуса
					print(f'\n{self.date()} <@{self.screen_name}> {Fore.GREEN}{title} {Fore.YELLOW}{self.token} {Fore.MAGENTA}{self.debug} {Fore.CYAN}{self.online} {Fore.BLUE}{self.friends}{Fore.RESET}')
				if self.debug == 1:
					print(f'{self.date()} <@{self.screen_name}> {Fore.GREEN}{title} {Fore.YELLOW}{self.token} {Fore.MAGENTA}{self.debug} {Fore.CYAN}{self.online} {Fore.BLUE}{self.friends}{Fore.RESET}')
				print(f"| {len(title)} / 140 символов")
			else:
				print(f'\n{self.date()} | статус @{self.screen_name} не может быть установлен из-за превышения лимита длинны в 140 символов')
				print(f'{len(title)} / 140 символов')
		except Exception as e:
			print(f'e: {Fore.YELLOW}{e}{Fore.RESET}')

		if self.online == 1:
			self.vk.method("account.setOnline") #отправляет запрос на установку статуса "Онлайн" на 5 минут
		else:
			self.vk.method("account.setOffline") # отправляет запрос на установку статуса "Оффлайн" каждые 5 минут

		#Удаление входящих заявок в друзья
		if self.friends == 1:
			self.vk.method("friends.deleteAllRequests") #удаляет все входящие заявки в друзья
