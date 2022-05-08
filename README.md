# Web_Crawler_Application
## 簡介
### 透過 [React](https://zh-hant.reactjs.org/) + [Nginx](https://nginx.org/en/) + [Django](https://www.djangoproject.com/) + [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) + [Redis](https://redis.io/) + [Mariadb](https://mariadb.org/) + [Rabbitmq](https://www.rabbitmq.com/) 架設一個爬蟲網站，讓使用者同時撈取 Ptt 文章資訊、股票資料，並在網頁上查看，以及將其匯出至 CSV 或 JSON 的檔案格式
<br>

### 手機板介面
##### 登入介面
![alt text](https://imgur.com/KGEQXP3.png)

##### Ptt 文章搜尋結果
![alt text](https://imgur.com/o1oajyD.png)

##### 功能選單 (查看, 匯出 CSV 或 JSON 檔案, 刪除)
![alt text](https://imgur.com/nYnMdgc.png)

##### 查看 Ptt 文章搜尋結果
![alt text](https://imgur.com/vExOmO0.png)

### 網頁版介面
![alt text](https://imgur.com/dPeROLS.png)
![alt text](https://imgur.com/WXOtH5u.png)

## 功能介紹
### Stock 爬蟲透過 Yahoo Finance API 撈取指定範圍時間的股價，並將撈取到的資料轉換成圖表以視覺化方式呈現

* 單個公司股價查詢 (台積電, ticker 2330.TW)
#### 查看股價
![alt text](https://imgur.com/2yOPOnR.png)
![alt text](https://imgur.com/qZkUGsI.png)

#### 圖表
Open Price
![alt text](https://imgur.com/m4jFlpH.png)

Volume
![alt text](https://imgur.com/fz0hPye.png)


* 多個公司股價查詢 (AMD && Intel, ticker: AMD,INTC)
#### 查看股價
![alt text](https://imgur.com/LfVysn0.png)

#### 圖表
Open Price
![alt text](https://imgur.com/itTfssJ.png)

Volume
![alt text](https://imgur.com/ZEkie2L.png)

### Ptt 爬蟲從 [Ptt](https://www.ptt.cc/bbs/index.html) 撈取各大熱門板的文章資料

![alt](https://imgur.com/T7KviqB.png)
![alt](https://imgur.com/JP85C3A.png)
![alt](https://imgur.com/DfWxXbN.png)
![alt](https://imgur.com/Yybtkpe.png)

## 有興趣的人，可以至下方的連結，用 demo 這組帳號登入測試
>> 此帳號僅供測試網路爬蟲抓取 Ptt 文章資訊與股票資料使用，用戶忘記密碼的功能，請自行註冊一組帳號測試

### 測試帳號 && 密碼
[Demo](https://hoshi-crawler.serveirc.com/)
```
    account: demo
    password: Demo21739865
```

### 帳號註冊

[Register Account](https://hoshi-crawler.serveirc.com/session/register)

![alt](https://imgur.com/1C9lF3K.png)



# 執行環境
* Linux
* Ubuntu 20.04
* Python 3.7.9