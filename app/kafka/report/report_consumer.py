from confluent_kafka import Consumer
from app.service.dog import DogService

from time import sleep


class ReportConsumer:
    broker = "localhost:9092"
    topic = "report-dog"
    group_id = "consumer-1"
    auto_commit = 'false'

    def start(self):

        conf = {'bootstrap.servers': self.broker,
                'group.id': self.group_id,
                'session.timeout.ms': 6000,
                'enable.auto.commit': True,
                'auto.offset.reset': 'earliest'
                }

        consumer = Consumer(conf)
        consumer.subscribe([self.topic])
        try:
            while True:
                msg = consumer.poll(0)
                if msg is None:
                    continue
                elif msg.error():
                    print('error: {}'.format(msg.error()))
                else:
                    record_value = msg.value().decode('utf-8')
                    print(f"Consumed {msg.topic()} record {record_value}")
                    service = DogService()
                    service.generate_report_pdf()
                sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            print("Leave group and commit final offsets")
            consumer.close()
