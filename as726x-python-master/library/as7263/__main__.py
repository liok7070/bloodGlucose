import as7263
import time
import os
import pandas as pd
import csv
from as7263 import AS7263

as7263 = AS7263()
as7263.set_measurement_mode(2)
as7263.set_illumination_led(1)

# 將資料寫入 CSV 檔
def write_to_csv(values):
    filename = '04.27.026_data1test.csv'
    # 如果檔案不存在，就先建立檔案並加上欄位名稱
    if not os.path.isfile(filename):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['R', 'S', 'T', 'U', 'V', 'W'])
    # 寫入資料
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(values)

# 讀取感測器資料
def read_sensor_data():
    i = 1
    as7263.soft_reset()

    hw_type, hw_version, fw_version = as7263.get_version()

    print('{}'.format(fw_version))

    as7263.set_gain(64)

    as7263.set_integration_time(17.857)

    as7263.set_measurement_mode(2)
    #修改1(on)或0(off)LED
    as7263.set_illumination_led(1)
    
    #as7262.set_illumination_led_current(12.5)
    #as7262.set_indicator_led_current(2)
    #as7262.set_indicator_led(1)
    
    # 如須讀取指定筆數,則使用while i < x ,x為數據筆
    try:
        while True:
            values = as7263.get_calibrated_values()
            print(str(i))
            print("R: {:.2f}, S: {:.2f}, T: {:.2f}, U: {:.2f}, V: {:.2f}, W: {:.2f}".format(*values))
            # 將資料寫入 CSV 檔
            write_to_csv(values)
            i += 1
            time.sleep(0.5)
            
    #按下ctrl+c退出終端機,並關掉設備白熾燈
    except KeyboardInterrupt:
        as7263.set_measurement_mode(3)
        #（0）為關燈指令
        as7263.set_illumination_led(0)

if __name__ == '__main__':
    # 啟動程式時讀取感測器資料
    read_sensor_data()
    # 使用者決定要暫停或開始讀取
    while True:
        user_input = input("輸入 'p' 暫停讀取，輸入 's' 開始讀取，輸入 'q' 結束程式：")
        if user_input == 'p':
            print("暫停讀取...")
            time.sleep(1)
        elif user_input == 's':
            print("開始讀取...")
            read_sensor_data()
        elif user_input == 'q':
            print("結束程式。")
            break
        else:
            print("輸入錯誤，請重新輸入。")
