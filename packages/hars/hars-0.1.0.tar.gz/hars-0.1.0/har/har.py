import json
import requests


class Har:
    def __init__(self, har_file_path: str):
        with open(har_file_path, 'r', encoding='utf-8') as file:
            self.har_data = json.load(file)
            self.log = self.har_data['log']
            self.version = self.log['version']
            self.pages = self.log['pages']
            self.creator = self.log['creator']
            self.entries = [Entry(entry) for entry in self.log['entries']]

    def replay(self, entry_index:int = 0):
        """
        重发指定索引的请求
        :param entry_index: 请求的索引，默认为0
        :return: 响应对象
        """
        entry = self.entries[entry_index]
        request = entry.request

        headers = {}
        for header in request['headers']:
            headers[header['name']] = header['value']

        cookies = {}
        for cookie in request['cookies']:
            cookies[cookie['name']] = cookie['value']

        params = {}
        for param in request['queryString']:
            params[param['name']] = param['value']

        data = request['postData']['text'] if 'postData' in request and 'text' in request['postData'] else None
        files = request['postData']['params'] if 'postData' in request and 'params' in request['postData'] else None
        if files:
            files = {file['name']: (file['fileName'], file['value']) for file in files}
        else:
            files = None
        if data:
            data = json.loads(data)
        else:
            data = None

        response = requests.request(
            request['method'],
            request['url'],
            headers=headers,
            cookies=cookies,
            params=params,
            data=data,
            files=files
        )
        return response


class Entry:
    def __init__(self, entry_json):
        self._entry = entry_json
        for key, value in entry_json.items():
            setattr(self, key, value)


def load(har_file_path: str):
    return Har(har_file_path)
