class DashaMailResponse:
    error_code: int
    error_message: str
    transaction_id: str = ''

    def __init__(self, response):

        if isinstance(response, str):
            self.error_other(response)
        else:
            data = response.json()
            response_type = data['response']['msg']['type']
            if response_type == 'message':
                self.success(data)
            elif response_type == 'error':
                self.error(data)
            else:
                self.error(data)

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
        self.error_code = -1000
        self.error_message = result
        print(self.__dict__)
