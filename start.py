import autostatus # импорт автостатуса
import time  # чтобы сделать задержку по времени

while True:
	auto = autostatus.status('ваш токен') # экземпляр класса автостатуса 
	auto.get_status(f'{auto.time} dreams') # текст автостатуса
	time.sleep(45) # задержка в секундах, лучше не трогать