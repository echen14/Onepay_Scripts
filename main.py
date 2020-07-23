import psycopg2
import requests
import json
import uuid

class MiniRefund:
    uri_pr = 'https://onepay-asia-api.subsidia.org/api/v2/payments/723/actions/do_refund'
    uri_pp = 'https://onepay-asia-api.preprod.subsidia.org/api/v2/payments/723/actions/do_refund'
    Database = 'onepaypr'
    DB_user = ['onepaypr', 'onepaypp']
    DB_pwd = ['onepaypr2019', 'onepaypp2018']
    DB_host = ['rtopn1pgs01.cuuxvcxw3hrr.rds.cn-north-1.amazonaws.com.cn', 'rtopv1pgs01.c0x6zghvypsc.rds.cn-north-1.amazonaws.com.cn', '127.0.0.1']
    DB_port = ['60901', '5901']

    def __init__(self, env, connection, orderId):
        self.env = env
        self.connection = connection
        self.orderId = orderId

    def get_uri(self):
        if self.env == 'PP':
            return MiniRefund.uri_pp
        elif self.env == 'PR':
            return MiniRefund.uri_pr
        else:
            print('Please input appointed value')

    def connect_method(self):
        if self.env == 'PP':
            # '0' ==>> direct
            if self.connection == '0':
                return MiniRefund.DB_user[1],MiniRefund.DB_pwd[1],MiniRefund.DB_host[1],MiniRefund.DB_port[0]
            # '1' ==>> gateway
            elif self.connection == '1':
                return MiniRefund.DB_user[1],MiniRefund.DB_pwd[1],MiniRefund.DB_host[2],MiniRefund.DB_port[1]
            else:
                print('You input the invalid number. Please retry')
        else:
            # '0' ==>> direct
            if self.connection == '0':
                return MiniRefund.DB_user[0], MiniRefund.DB_pwd[0], MiniRefund.DB_host[0], MiniRefund.DB_port[0]
            # '1' ==>> gateway
            elif self.connection == '1':
                return MiniRefund.DB_user[0], MiniRefund.DB_pwd[0], MiniRefund.DB_host[2], MiniRefund.DB_port[1]
            else:
                print('You input the invalid number. Please retry')

    def process(self):
        new_id = self.orderId.split(',')
        id = ','.join(new_id)
        return id

    def get_transactions(self):
        conn = psycopg2.connect(database=MiniRefund.Database, user=MiniRefund.connect_method(self)[0], password=MiniRefund.connect_method(self)[1],
                                host=MiniRefund.connect_method(self)[2], port=MiniRefund.connect_method(self)[3])
        cur = conn.cursor()
        sql = """
        select distinct(t.order_id), t.transact_id, td.td_amount, tl.tlog_value from transaction t
        join transaction_detail td on td.transact_id = t.transact_id
        join transaction_logs tl on tl.td_id = td.td_id
        where tl.tlog_key = 'pspTransactionId'
        and t.ts_id = 28
        and t.order_id in ({})
        """.format(MiniRefund.process(self))
        cur.execute(sql)
        data = cur.fetchall()
        return data

    def send_request(self):
        headers = {'Content-Type': 'application/json'}
        for info in MiniRefund.get_transactions(self):
            payload_dic = {
                'client_name': 'CUBECN',
                'channel': 'MINIPROGRAM',
                'transaction_id': info[1],
                'contract_attributes': [
                    {
                        'conatt_key': 'externalActionId',
                        'conatt_value': str(uuid.uuid4())
                    },
                    {
                        'conatt_key': 'orderId',
                        'conatt_value': info[0]
                    },
                    {
                        'conatt_key': 'refundAmount',
                        'conatt_value': str(info[2])
                    },
                    {
                        'conatt_key': 'pspTransactionId',
                        'conatt_value': info[3]
                    },
                    {
                        'conatt_key': 'total_fee',
                        'conatt_value': str(int(info[2]*100))
                    }]
            }

            payload = json.dumps(payload_dic).encode(encoding='utf-8')
            response = requests.request("POST", MiniRefund.get_uri(self), headers=headers, data=payload)

            print(response.text.encode('utf8'))

if __name__ == '__main__':
    pass