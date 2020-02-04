import sys, csv
from PyQt5.QtCore import QObject, QDateTime
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget

class csvWriter(QObject):
    def __init__(self, parent):
        super(csvWriter, self).__init__(parent)
        self.parentWidget = parent
        self.csvfile = None

    def start_writing(self) -> bool:
        '''接口函数，选择文件路径，并打开文件准备写入

        供主程序调用，返回打开文件是否成功
        '''
        # 选择文件路径
        filename = QFileDialog.getSaveFileName(self.parentWidget, "choose a path to save file", 
        QDateTime.currentDateTime().toString("yyyyMMdd-HHmm") + ".csv", "csv files(*.csv)")
        if filename[0] == "":
            return False
        # 打开文件
        self.csvfile = open(filename[0], mode = "w", newline = "")
        return True



    def write_distances(self, curTime: int, distances: list, curAngle: float) -> bool:
        '''接口函数，在指定文件写入一行数据，包括当前时间，三个距离值，以及角度值

        供主程序调用，返回写入是否成功
        '''
        writer = csv.writer(self.csvfile)
        writer.writerow([curTime] + distances + [curAngle])
        return True

    def stop_writing(self) -> bool:
        '''接口函数，停止写入，关闭文件

        供主程序调用，返回关闭是否成功
        '''
        self.csvfile.close()
        self.csvfile = None
        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.show()
    dataWriter = csvWriter(window)
    # ----
    dataWriter.start_writing()
    dataWriter.write_distances(1,[3,2,1], 1.0)
    dataWriter.write_distances(2,[1,2,3], 1.0)
    dataWriter.write_distances(2,[1,2,3], 1.0)
    dataWriter.stop_writing()
    # ----
    sys.exit(app.exec_())
