class DashaMailResponse:
    http_status_code: int
    error_code: int
    error_message: str
    transaction_id: str = ''

    def __init__(self, response):

        if isinstance(response, str):
            self.error_other(response)
        else:
            self.http_status_code = response.status_code
            response_json = response.json()
            response_type = response_json['response']['msg']['type']
            if self.http_status_code == 200:
                if response_type == 'message':
                    self.success(response_json)
                elif response_type == 'error':
                    self.error(response_json)
            else:
                self.error(response_json)

    def success(self, data):
        self.error_code = data['response']['msg']['err_code']
        self.error_message = data['response']['msg']['text']
        self.transaction_id = data['response']['data']['transaction_id']
        print(self.__dict__)

    def error(self, data):
        self.error_code = data['response']['msg']['err_code']
        self.error_message = data['response']['msg']['text']
        print(self.__dict__)

    def error_other(self, result):
        self.http_status_code = 400
        self.error_code = -1000
        self.error_message = result
        print(self.__dict__)
