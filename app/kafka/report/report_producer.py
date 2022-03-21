from confluent_kafka import Producer


class ReportProducer:
    broker = "localhost:9092"
    topic = "report-dog"

    def delivery_callback(self, err, msg):
        if err:
            print(f"Message failed delivery error: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}")

    def send(self, msg):
        config = {
            'bootstrap.servers': self.broker,
        }
        producer = Producer(config)
        producer.produce(self.topic, str(msg).encode('utf-8'), callback=self.delivery_callback)
        producer.flush()
