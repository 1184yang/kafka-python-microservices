from threading import Thread
import sauce_service
import cheese_service
import meat_service
import veggie_service

sauce_t = Thread(target=sauce_service.start_service)
cheese_t = Thread(target=cheese_service.start_service)
meat_t = Thread(target=meat_service.start_service)
veggie_t = Thread(target=veggie_service.start_service)

sauce_t.start()
cheese_t.start()
meat_t.start()
veggie_t.start()
