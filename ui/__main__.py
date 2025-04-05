import PySide6.QtCore;
import sys,random,os,shutil;
from PySide6 import QtCore,QtWidgets,QtGui;

#template project: to update to actually work, but later.
#i want to prioritize the cli and make the ui functional later

class _App(QtWidgets.QWidget):
  def __init__(self):
    super().__init__();
    self.hello=["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"];
    self.button=QtWidgets.QPushButton("Click me!");
    self.text=QtWidgets.QLabel("Hello World",alignment=QtCore.Qt.AlignCenter);
    self.layout=QtWidgets.QVBoxLayout(self);
    self.layout.addWidget(self.text);
    self.layout.addWidget(self.button);
    self.button.clicked.connect(self.magic);
    
  @QtCore.Slot()
  def magic(self):
    self.text.setText(random.choice(self.hello));

def StartApp():
  app=QtWidgets.QApplication([]);

  widget=_App();
  widget.resize(800,600);
  widget.show();

  sys.exit(app.exec());

StartApp();