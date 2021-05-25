# Compal Cloud Gaming Manager
____________________________________________
## 環境設定
* **python 環境和套件安裝**

安裝完 python3 後，安裝相關 python 套件
1. 使用 pipenv 安裝相關套件 [參考文章](https://medium.com/@chihsuan/pipenv-%E6%9B%B4%E7%B0%A1%E5%96%AE-%E6%9B%B4%E5%BF%AB%E9%80%9F%E7%9A%84-python-%E5%A5%97%E4%BB%B6%E7%AE%A1%E7%90%86%E5%B7%A5%E5%85%B7-135a47e504f4)
  
`pipenv lock` ：當沒有Pipfile.lock 時，根據當下 virtualenv 資料夾中所有套件的版本，生成新的 Pipfile.lock 檔。

`pipenv sync `：安裝所有 Pipfile.lock 中指定的版本套件。

2. 或使用 pip 管理

`pip install virtualenv` : 安裝virtualenv

`virtualenv env`  : 創建新環境

`activate` : 啟動安裝環境 *(至activate檔所在file)*

`pip list` : 顯示 pip 安裝目錄

`pip install -r requirements.txt` : 從requirements.txt安裝 site-pkg

* **安裝 MySQL 和 MySQLWorkbench**

1. 安裝完 MySQL 和 MySQLWorkbench 後，如果沒有還沒有建置 DB，可以透過 Workbench 的 data import 功能，將 `db_replica.sql` 匯入至 MySQL 中，[教學網站在此](https://mnya.tw/cc/word/1395.html)
  

2. 需要在 /manager/config.py 中更改連線資料庫帳密和 IP address
  
`SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{IP address}:{port}/cloud_game_db"`

username: compal_admin
<br>password: admin
<br>IP: 10.113.8.192
<br>port: 3306
_____________________________________________
## 運行 Control Panel
兩種方法
1. 在 cmd 輸入 `pipenv run python3 run.py`
2. 點擊 start.bat 程式自動進入 virualenv 並運行 flask

從瀏覽器輸入 `{IP address}:5001` 即可看到登入頁面 ( port 號可以在 run.py 更改 )

平台預設帳密: Compal Admin/ admin

可以使用 MySQLWorkbench 檢視資料庫 schema 和資料
