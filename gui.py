from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, os, subprocess
import netifaces
from services import WaitingMessage


class index(QDialog):
	def __init__(self, parent=None):
		super(index, self).__init__(parent)
		
		labelTopic = QLabel("Topic exchange exigido: ")
		self.fieldTopic = QLineEdit()
		labelBrokerIP = QLabel("Host do broker message")
		self.fieldBrokerIP = QLineEdit()

		hboxSettings = QHBoxLayout()
		hboxSettings.addWidget(labelTopic)
		hboxSettings.addWidget(self.fieldTopic)
		hboxSettings.addWidget(labelBrokerIP)
		hboxSettings.addWidget(self.fieldBrokerIP)

		self.buttonStartConsumer = QPushButton("Start consumer!")

		labelListMessage = QLabel("Lista de mensagens recebidas:")

		self.listMessage = QListWidget()

		vboxAll = QVBoxLayout()
		vboxAll.addLayout(hboxSettings)
		vboxAll.addWidget(self.buttonStartConsumer)
		vboxAll.addWidget(labelListMessage)
		vboxAll.addWidget(self.listMessage)

		
		self.thConsumer = WaitingMessage(self.fieldTopic.displayText(), self.fieldBrokerIP.displayText(), self.listMessage)

		self.connect(self.buttonStartConsumer, SIGNAL("clicked()"), self.evt_consumer)
		#self.connect(self.buttonStartBroker, SIGNAL("clicked()"), self.clean_messages)
		self.setLayout(vboxAll)
		self.setWindowTitle("Consumer")
		self.setGeometry(300,100,700,430)

	def evt_consumer(self):
		if self.fieldTopic.displayText() != '' or self.fieldBrokerIP.displayText() != '':
			try:
				self.buttonStartConsumer.setText("Aguardando por mensagens de {}...".format(self.fieldBrokerIP.displayText()))
				#self.buttonStartConsumer.setEnabled(False)	
				self.fieldTopic.setEnabled(False)
				self.fieldBrokerIP.setEnabled(False)
				self.buttonStartConsumer.setEnabled(False)
				self.thConsumer.start()
			except Exception as e:
				msg = QMessageBox.information(self, "Erro!",
											"Informe os valores corretos",
											 QMessageBox.Close)
				print(e)


app = QApplication(sys.argv)
dlg = index()
dlg.exec_()