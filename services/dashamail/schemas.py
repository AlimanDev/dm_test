class DashaMailResponse:
    status_code: int
    err_code: int
    text: str
    _type: str
    transaction_id: str

    def __init__(self, result):
        self.status_code = result.status_code
        if self.status_code == 200:
            resp_data = result.json()
            response = resp_data.get('response')
            msg = response.get('msg')
            data = response.get('data')
            self.err_code = msg.get('err_code')
            self.text = msg.get('text')
            self._type = msg.get('type')
            self.transaction_id = data.get('transaction_id')
