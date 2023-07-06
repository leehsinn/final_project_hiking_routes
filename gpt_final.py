from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
from twomainwindow import Ui_Dialog
import sys
import time

df = pd.read_excel('final_all_trails.xlsx', sheet_name='tryui')

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.search)
        self.ui.pushButton_go.clicked.connect(self.go)
        self.ui.pushButton_taipei.clicked.connect(self.taipei)
        self.ui.pushButton_3000up.clicked.connect(self.veryhigh)
        self.ui.pushButton_weekend.clicked.connect(self.weekend)
        self.ui.pushButton_train.clicked.connect(self.train)
        self.ui.comboBox.addItems(['全部', '台北市', '新北市', '桃園市', '新竹市', '新竹縣', '苗栗縣', '台中市', '彰化縣', '南投縣', '雲林縣', '嘉義市', '嘉義縣', '台南市', '高雄市', '屏東縣', '宜蘭縣', '花蓮縣', '台東縣', '澎湖縣', '金門縣', '連江縣'])
        self.ui.spinBox_gap.setRange(0,2000)
        self.ui.spinBox_gap.setSingleStep(200)
        self.ui.spinBox_gap.setValue(0)
        self.ui.spinBox_height.setRange(0,3000)
        self.ui.spinBox_height.setSingleStep(200)
        self.ui.spinBox_height.setValue(0)
        group1 = QButtonGroup(self) 
        group1.addButton(self.ui.radioButton_high)
        group1.addButton(self.ui.radioButton_low)

    def go(self):
        x = self.ui.lineEdit.text()
        name_select = df[df['步道名稱'].str.contains(x)][['步道名稱', '所在縣市1', '海拔','步道攀登所需時間']] 
        table_widget = QTableWidget()
        table_widget.setRowCount(name_select.shape[0])
        table_widget.setColumnCount(name_select.shape[1])

        table_widget.setHorizontalHeaderLabels(name_select.columns)

        for i, row in enumerate(name_select.values):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                table_widget.setItem(i, j, item)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(table_widget)
        
        dialog = QDialog()
        dialog.resize(480, 400)
        layout = QVBoxLayout(dialog)
        layout.addWidget(scroll_area)
        dialog.setLayout(layout)
        dialog.setWindowTitle("步道搜尋")
        dialog.exec_()


    def taipei(self):
        taipei_trails = df[df['步道名稱'].str.contains("台北大縱走")][['步道名稱','步道相關資訊網站']] 
        order = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8}
        taipei_trails['排序'] = taipei_trails['步道名稱'].str.extract('第(\w+)段', expand=False).map(order)
        sorted_trails = taipei_trails.sort_values(by='排序')
        # 創建QTableWidget並設置行列數
        table_widget = QTableWidget()
        table_widget.setRowCount(sorted_trails.shape[0])
        table_widget.setColumnCount(sorted_trails.shape[1]-1)

        header_labels = [col for col in taipei_trails.columns if col != '排序']
        table_widget.setHorizontalHeaderLabels(header_labels)
        table_widget.horizontalHeader().setDefaultSectionSize(430)

        # 設置表格內容（排除 '排序' 列）
        for i, row in enumerate(taipei_trails.values):
            row_values = [value for j, value in enumerate(row) if j != taipei_trails.columns.get_loc('排序')]
            for j, value in enumerate(row_values):
                item = QTableWidgetItem(str(value))
                table_widget.setItem(i, j, item)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(table_widget)
        
        # 創建對話方塊並設置內容
        dialog = QDialog()
        dialog.resize(480, 400)
        layout = QVBoxLayout(dialog)
        layout.addWidget(scroll_area)
        dialog.setLayout(layout)
        dialog.setWindowTitle("台北大縱走")
        dialog.exec_()   


    def veryhigh(self):
        df['步道海拔高'] = pd.to_numeric(df['步道海拔高'], errors='coerce')
        #high3 = df[df['步道海拔高'] >= 3000][['步道名稱', '所在縣市1', '海拔','步道攀登所需時間']] 
        high3 = df[df['步道海拔高'] >= 3000].sort_values(by='造訪人數', ascending=False)[['步道名稱', '所在縣市1', '海拔','步道攀登所需時間']]

        table_widget = QTableWidget()
        table_widget.setRowCount(high3.shape[0])
        table_widget.setColumnCount(high3.shape[1])

        table_widget.setHorizontalHeaderLabels(high3.columns)

        for i, row in enumerate(high3.values):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                table_widget.setItem(i, j, item)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(table_widget)
        
        dialog = QDialog()
        dialog.resize(600, 400)
        layout = QVBoxLayout(dialog)
        layout.addWidget(scroll_area)
        dialog.setLayout(layout)
        dialog.setWindowTitle("入門百岳推薦")
        dialog.exec_()


    def weekend(self):
        country = self.ui.comboBox.currentText()
        df['造訪人數'] = pd.to_numeric(df['造訪人數'], errors='coerce')
        df['步道海拔高'] = pd.to_numeric(df['步道海拔高'], errors='coerce')        
        if country == "全部":
            easy = df[(df['步道海拔高'] <= 2500) & (df['造訪人數'] >= 2000) &  (df['步道難易度'] <= 2)].sort_values(by='造訪人數', ascending=False)[['步道名稱', '所在縣市1', '海拔','步道攀登所需時間']] 
        else: 
            search_columns = ['所在縣市1', '所在縣市2', '所在縣市3']
            easy = df[(df[search_columns].isin([country]).any(axis=1))&(df['步道海拔高'] <= 2000) & (df['造訪人數'] >= 2000) &  (df['步道難易度'] <= 2)].sort_values(by='造訪人數', ascending=False)[['步道名稱', '所在縣市1', '海拔','步道攀登所需時間']]    
        
        table_widget = QTableWidget()
        table_widget.setRowCount(easy.shape[0])
        table_widget.setColumnCount(easy.shape[1])

        table_widget.setHorizontalHeaderLabels(easy.columns)

        for i, row in enumerate(easy.values):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                table_widget.setItem(i, j, item)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(table_widget)
        
        dialog = QDialog()
        dialog.resize(600, 400)
        layout = QVBoxLayout(dialog)
        layout.addWidget(scroll_area)
        dialog.setLayout(layout)
        dialog.setWindowTitle("郊山步道推薦")
        dialog.exec_()        
         

    def train(self):
        country = self.ui.comboBox.currentText()
        df['步道海拔高'] = pd.to_numeric(df['步道海拔高'], errors='coerce')
        df['高度落差'] = pd.to_numeric(df['高度落差'], errors='coerce')
        df['所需時間'] = pd.to_numeric(df['所需時間'], errors='coerce')
        if country == "全部":
            tired = df[(df['步道海拔高'] < 3000) & (df['高度落差'] > 500) & (df['所需時間'] >= 300) & (df['所需時間'] <= 650)].sort_values(by='造訪人數', ascending=False)[['步道名稱', '所在縣市1', '海拔', '高度落差','步道攀登所需時間']] 
        else: 
            search_columns = ['所在縣市1', '所在縣市2', '所在縣市3']
            tired = df[(df[search_columns].isin([country]).any(axis=1))&(df['步道海拔高'] < 3000) & (df['高度落差'] > 500) & (df['所需時間'] >= 300) & (df['所需時間'] <= 650)].sort_values(by='造訪人數', ascending=False)[['步道名稱', '所在縣市1', '海拔', '高度落差','步道攀登所需時間']] 

        table_widget = QTableWidget()
        table_widget.setRowCount(tired.shape[0])
        table_widget.setColumnCount(tired.shape[1])

        table_widget.setHorizontalHeaderLabels(tired.columns)

        for i, row in enumerate(tired.values):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                table_widget.setItem(i, j, item)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(table_widget)
        
        dialog = QDialog()
        dialog.resize(480, 400)
        layout = QVBoxLayout(dialog)
        layout.addWidget(scroll_area)
        dialog.setLayout(layout)
        dialog.setWindowTitle("練腳步道推薦")
        dialog.exec_()   


    def search(self):
        country = self.ui.comboBox.currentText()
        gap = self.ui.spinBox_gap.value()
        lowheight = 0
        if self.ui.radioButton_low.isChecked():
            lowheight = self.ui.spinBox_height.value()
            highheight = lowheight

        elif self.ui.radioButton_high.isChecked():
            lowheight = 0
            highheight = self.ui.spinBox_height.value() 
        else:
            highheight = lowheight

        #name_rough_select = df[df["步道名稱"].str.contains(x)][["步道名稱","縣市"]]
        df['高度落差'] = pd.to_numeric(df['高度落差'], errors='coerce')
        df['步道海拔低'] = pd.to_numeric(df['步道海拔低'], errors='coerce')
        df['步道海拔高'] = pd.to_numeric(df['步道海拔高'], errors='coerce')  

        if country == '全部':
            all_country = df[(df['高度落差'] > gap) & (df['步道海拔低'] > lowheight) & (df['步道海拔高'] > highheight)][['步道名稱', '所在縣市1', '海拔','所需時間','步道攀登所需時間']]
            all_country['所需時間'] = pd.to_numeric(all_country['所需時間'], errors='coerce')
            if self.ui.radioButton_all.isChecked(): 
                final_select = all_country
            elif self.ui.radioButton_3hours.isChecked():
                final_select = all_country[(all_country['所需時間'] <= 180)][['步道名稱', '所在縣市1', '海拔','步道攀登所需時間']] 
            elif self.ui.radioButton_3to6.isChecked():
                final_select = all_country[(all_country['所需時間'] > 180) & (all_country['所需時間'] <= 360)][['步道名稱', '所在縣市1', '海拔','步道攀登所需時間']]    
            elif self.ui.radioButton_6to12.isChecked():
                final_select = all_country[(all_country['所需時間'] > 360) & (all_country['所需時間'] <= 720)][['步道名稱', '所在縣市1', '海拔','步道攀登所需時間']]
            elif self.ui.radioButton_12to2days.isChecked():
                final_select = all_country[(all_country['所需時間'] > 720) & (all_country['所需時間'] <= 2880)][['步道名稱', '所在縣市1', '海拔','步道攀登所需時間']]
            elif self.ui.radioButton_2days.isChecked():
                final_select = all_country[all_country['所需時間'] > 2880][['步道名稱', '所在縣市1', '海拔','步道攀登所需時間']]
            else:
                # 未選擇任何選項，顯示提示訊息框
                message = QMessageBox()
                message.setWindowTitle("選擇錯誤")
                message.setText("請選擇一個範圍選項")
                message.setIcon(QMessageBox.Warning)
                message.exec_()
                return             

        else:
            search_columns = ['所在縣市1', '所在縣市2', '所在縣市3']
            all_country = df[(df[search_columns].isin([country]).any(axis=1)) & (df['高度落差'] > gap) & (df['步道海拔低'] > lowheight) & (df['步道海拔高'] > highheight)][['步道名稱', '所在縣市1', '海拔','所需時間','步道攀登所需時間']]
            all_country['所需時間'] = pd.to_numeric(all_country['所需時間'], errors='coerce')
            if self.ui.radioButton_all.isChecked(): 
                final_select = all_country
            elif self.ui.radioButton_3hours.isChecked():
                final_select = all_country[(all_country['所需時間'] <= 180)][['步道名稱', '所在縣市1', '海拔','步道攀登所需時間']] 
            elif self.ui.radioButton_3to6.isChecked():
                final_select = all_country[(all_country['所需時間'] > 180) & (all_country['所需時間'] <= 360)][['步道名稱', '所在縣市1', '海拔','步道攀登所需時間']]    
            elif self.ui.radioButton_6to12.isChecked():
                final_select = all_country[(all_country['所需時間'] > 360) & (all_country['所需時間'] <= 720)][['步道名稱', '所在縣市1', '海拔','步道攀登所需時間']]
            elif self.ui.radioButton_12to2days.isChecked():
                final_select = all_country[(all_country['所需時間'] > 720) & (all_country['所需時間'] <= 2880)][['步道名稱', '所在縣市1', '海拔','步道攀登所需時間']]
            elif self.ui.radioButton_2days.isChecked():
                final_select = all_country[all_country['所需時間'] > 2880][['步道名稱', '所在縣市1', '海拔','步道攀登所需時間']]
            else:
                # 未選擇任何選項，顯示提示訊息框
                message = QMessageBox()
                message.setWindowTitle("選擇錯誤")
                message.setText("請選擇一個範圍選項")
                message.setIcon(QMessageBox.Warning)
                message.exec_()
                return       


        table_widget = QTableWidget()
        table_widget.setRowCount(final_select.shape[0])
        table_widget.setColumnCount(final_select.shape[1])

        table_widget.setHorizontalHeaderLabels(final_select.columns)

        for i, row in enumerate(final_select.values):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                table_widget.setItem(i, j, item)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(table_widget)
        
        dialog = QDialog()
        dialog.resize(480, 400)
        layout = QVBoxLayout(dialog)
        layout.addWidget(scroll_area)
        dialog.setLayout(layout)
        dialog.setWindowTitle("客製化找步道")
        dialog.exec_()     

input('請按enter執行畫面')
app = QApplication(sys.argv)
widget = MyWidget()
widget.show()
sys.exit(app.exec_())
