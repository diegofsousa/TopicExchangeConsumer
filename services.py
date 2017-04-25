from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os
import sys
import pika

class WaitingMessage(QThread):
	def __init__ (self, topic, brokerHost, guiList, parent=None):
		self.topic = topic
		self.brokerHost = brokerHost
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.brokerHost))
		self.channel = self.connection.channel()
		QThread.__init__(self)		

	def run(self):
		print(self.brokerHost)
		print(self.topic)
		

		self.channel.exchange_declare(exchange='topic_logs',
		                         type='topic')

		result = self.channel.queue_declare(exclusive=True)
		queue_name = result.method.queue

		binding_keys = self.topic

		for binding_key in binding_keys:
			self.channel.queue_bind(exchange='topic_logs',
			                   queue=queue_name,
			                   routing_key=binding_key)

		print(' [*] Waiting for logs. To exit press CTRL+C')

		def callback(ch, method, properties, body):
			item = QListWidgetItem("Topic: "+method.routing_key+" - Mensagem: "+body.decode("utf-8"))

			self.guiList.addItem(item)
			self.num += 1
			self.labelNum.setText("Numero de mensagens processadas: "+str(self.num))

			print(" [x] {} - {}".format(method.routing_key, body.decode("utf-8")))

		self.channel.basic_consume(callback,
		                      queue=queue_name,
		                      no_ack=True)

		self.channel.start_consuming()

	def close_wm(self):
		self.connection.close()
