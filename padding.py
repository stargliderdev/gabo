import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser

class PaddingExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Padding Example')
        self.setGeometry(100, 100, 800, 600)

        text_browser = QTextBrowser(self)
        text_browser.setOpenExternalLinks(True)

        html_content = """
        <html>
        <head>
            <style>
                .padded-content {
                    padding: 20px; /* Adjust the padding value as needed */
                }
            </style>
        </head>
        <body>
            <div class="padded-content">
                <h1>Content with Padding</h1>
                <p>This content has padding applied to it.</p>
            </div>
        </body>
        </html>
        """

        text_browser.setHtml(html_content)

        self.setCentralWidget(text_browser)

def main():
    app = QApplication(sys.argv)
    viewer = PaddingExample()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
