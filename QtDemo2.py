import sys
import pymysql
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.connection = self.connectToDatabase()
        self.createTable()

    def initUI(self):
        self.setWindowTitle("登录界面")

        # 登录部分
        self.usernameLabel = QLabel("用户名：", self)
        self.usernameEdit = QLineEdit(self)
        self.passwordLabel = QLabel("密码：", self)
        self.passwordEdit = QLineEdit(self)
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.loginButton = QPushButton("登录", self)
        self.loginButton.clicked.connect(self.login)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.usernameLabel)
        layout.addWidget(self.usernameEdit)
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordEdit)
        layout.addWidget(self.loginButton)

        self.setLayout(layout)
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def connectToDatabase(self):
        try:
            connection = pymysql.connect(
                host='mysql.sqlpub.com',
                user='lanteriso',
                password='FJBEpV3e47W7eoJ6',
                db='lanteriso',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)
            return connection
        except pymysql.MySQLError as e:
            print(f"Error connecting to MySQL Platform: {e}")
            sys.exit()

    def createTable(self):
        with self.connection.cursor() as cursor:
            sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(50) NOT NULL
            )
            """
            cursor.execute(sql)
            self.connection.commit()

    def login(self):
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))
            result = cursor.fetchone()
            if result:
                QMessageBox.information(self, "登录成功", "欢迎回来！")
            else:
                QMessageBox.warning(self, "登录失败", "用户名或密码错误！")


def main():
    app = QApplication(sys.argv)
    ex = LoginWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()