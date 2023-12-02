from collections import deque
from concurrent.futures import ThreadPoolExecutor
import threading
import time
from typing import Deque, Dict

from event import Event
from event_result import EventResult
from utils import Utils


class EventLoop:

    def __init__(self) -> None:
        self.__event_queue: Deque[Event] = deque([])
        self.__handlers: Dict[str, callable] = {}
        self.__processed_events: Deque[EventResult] = deque([])

    def on(self, event: str, handler: callable):
        self.__handlers[event] = handler
        return self

    def dispatch(self, event: Event) -> None:
        self.__event_queue.append(event)

    def process_async(self, event: Event) -> None:
        # self.__processed_events.append(EventResult(event.key, self.__handlers.get(event.key)(*event.data)))
        
        def task():
            handler = self.__handlers.get(event.key)
            result = handler(event.data)
            processed_event = EventResult(event.key, result)
            with threading.Lock():
                self.__processed_events.append(processed_event)

        executor.submit(task)

    def process_sync(self, event: Event) -> None:
        self.produce_output_for(EventResult(event.key, self.__handlers.get(event.key)(event.data)))

    def produce_output_for(self, event_result: EventResult):
        print(event_result.result)

    def run(self):
        try:
            event = self.__event_queue.popleft()
            if event.key in self.__handlers:
                start_time = time.perf_counter()
                if event.asynchronous:
                    self.process_async(event)
                else:
                    self.process_sync(event)
                end_time = time.perf_counter()
                print("Event loop was blocked for: ", end_time - start_time)
            else:
                print("No handler found for event: ", event.key)
        except IndexError:
            # print("No pending events")
            pass

        try:
            processed_event = self.__processed_events.popleft()
            self.produce_output_for(processed_event)
        except IndexError:
            # print("No results")
            pass


def main():
    event_loop = EventLoop()
    utils = Utils()
    eventId = 0
    url = 'https://jsonplaceholder.typicode.com/posts/1'

    while True:
        print("What kind of task would you like to submit to the Event Loop?")
        print(" 1. Wish me Hello")
        print(" 2. Print the contents of a file named hello.txt")
        print(" 3. Retrieve a random JSON from the internet & print it")
        print(" 4. Print output of previously submitted asynchronous task")
        print(" 5. Exit!")
        usersChoice = input(" > ")

        operationType = "1"

        if usersChoice != "4" and utils.user_has_not_chosen_to_exit(usersChoice):
            print("How would you like to execute this operation?")
            print(" 1. Synchronously (this would block the Event Loop until the operation completes)")
            print(" 2. Asynchronously (this won't block Event Loop in any way)")
            operationType = input(" > ")

        uniqueEventKey = ""

        if usersChoice == "1":
            uniqueEventKey = utils.generate_unique_event_key("hello", eventId)
            eventId += 1
            event_loop.on(uniqueEventKey, lambda data: f"Hello! {data}").dispatch(Event(uniqueEventKey, "How are you doing today?", utils.is_asynchronous(operationType)))
        elif usersChoice == "2":
            uniqueEventKey = utils.generate_unique_event_key("read-file", eventId)
            eventId += 1
            event_loop.on(uniqueEventKey, utils.read_file).dispatch(Event(uniqueEventKey, "hello.txt", utils.is_asynchronous(operationType)))
        elif usersChoice == "3":
            uniqueEventKey = utils.generate_unique_event_key("fetch-random-json", eventId)
            eventId += 1
            event_loop.on(uniqueEventKey, utils.fetch_random_json).dispatch(Event(uniqueEventKey, url, utils.is_asynchronous(operationType)))
        elif usersChoice == "4":
            pass
        elif usersChoice == "5" or not usersChoice:
            break

        event_loop.run()


if __name__ == "__main__":
    with ThreadPoolExecutor(8) as executor:
        main()
