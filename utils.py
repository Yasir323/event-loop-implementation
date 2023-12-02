import json
import random
from typing import Union
import urllib3


class Utils:

    def __init__(self):
        self.random = random.Random()

    def read_file(self, file_name: str) -> str:
        lines = []

        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError as e:
            print(e)

        return ''.join(lines)

    def fetch_random_json(self, url: str) -> dict:
        http = urllib3.PoolManager()
        print("DOWNLOADING...")
        try:
            response = http.request('GET', url)
            if response.status == 200:
                data = json.loads(response.data.decode('utf-8'))
                return data
            else:
                print(f"Failed to fetch data. Status code: {response.status}")
        except urllib3.exceptions.HTTPError as e:
            print(f"HTTPError: {e}")
        except urllib3.exceptions.RequestError as e:
            print(f"RequestError: {e}")
        
        return {}


    @staticmethod
    def generate_unique_event_key(human_readable_event_key: str, event_count: int) -> str:
        return f"{human_readable_event_key}-{event_count}"

    @staticmethod
    def news_items_are_available(news_items: Union[dict, None]) -> bool:
        return news_items and 'results' in news_items and news_items['results']

    @staticmethod
    def is_asynchronous(operation_type: str) -> bool:
        return operation_type == "2"

    @staticmethod
    def user_has_not_chosen_to_exit(user_choice: str) -> bool:
        return user_choice != "5"
