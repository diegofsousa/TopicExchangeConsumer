from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os
import sys
import pika

class WaitingMessage(QThread):
	def __init__ (self, topic, brokerHost, guiList, parent=None):
		self.topic = topic
		self.brokerHost = brokerHost
		self.guiList = guiList
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.brokerHost))
		self.channel = self.connection.channel()
		QThread.__init__(self)		

	def run(self):
		print("era pra aparecer aqui")
		print(self.brokerHost)
		print(self.topic)
		

		self.channel.exchange_declare(exchange='topic_logs',
		                         type='topic')

		result = self.channel.queue_declare(exclusive=True)
		queue_name = result.method.queue

		binding_key = self.topic
		print(binding_key)

		self.channel.queue_bind(exchange='topic_logs',
		                   queue=queue_name,
		                   routing_key=binding_key)

		print(' [*] Waiting for logs. To exit press CTRL+C')

		def callback(ch, method, properties, body):
			item = QListWidgetItem("Topico: " + method.routing_key + " - Mensagem: " + body.decode("utf-8"))
			self.guiList.addItem(item)
			print(" [x] {} - {}".format(method.routing_key, body.decode("utf-8")))

		self.channel.basic_consume(callback,
		                      queue=queue_name,
		                      no_ack=True)

		self.channel.start_consuming()

	def close_wm(self):
		self.connection.close()
