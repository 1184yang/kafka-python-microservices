#### 快速的數據

快速數據似乎是技術領域中較新的談論主題，而其真正的價值集中在與僅靠大數據的承諾不同。Apache Kafka 漸漸被納入一般的資訊設計流程中，傳統的資料介面變成了 Kafka，而不是眾多的 REST 、GraphQL API 和資料庫。甚至也可以取代資料倉儲的 ETL。

大數據造就了眾多的微服務(Microservices)，這些微服務過去透過 REST 等 API 相互通訊，但現在可以利用 Kafka 透過事件在非同步服務之間進行通訊。微服務可以使用 Kafka 作為交互接口，而不是透過特定的 API 呼叫。Kafka 現在將自己定位為允許開發人員快速獲取資料的基礎上，即使大數據也需要有快速的回應。

Kafka Streams 現在可能是許多人開始工作時的預設選擇，但到 2016 年 Streams API 發佈時，Kafka 已經將自己確立為成功的解決方案。他主要的抽象層客戶端程式庫，包含 Producer 與 Consumer，用來傳送與接收資料，它提供了將資料作為無界流處理的更高層級視圖。

物聯網設備的數量只會隨著時間的推移而增加。由於所有這些設備都會發送訊息，因此需要有某種設備能夠有效地處理這些數據。大量數據正是 Kafka 擅長的領域。使用 Kafka 在目的地之間持續流動資料可以幫助我們重新設計過去僅限於批次或延時工作流程的系統。

事件是一種包含通知和狀態的邏輯構造，它告訴我們發生了什麼事，並為我們提供了有關發生的事情的資訊。 在 Kafka 中，事件由生產者(Producer)發佈到主題(Topic)並由消費者(Consumer)接收。 這些生產者和消費者不需要互相了解任何資訊。這個範例讓我們看看在連接微服務(Microservices)時如何利用這一點。

它可以向 Kafka 主題(Topic)產生一個事件，而不是一個應用程式透過 HTTP 呼叫另一個應用程式。另一個應用程式或多個其他應用程式可以同時使用該事件並採取某些操作。 然後，這些應用程式可以依次為其他主題產生新事件，可以繼續往下游進行操作，或作為最終結果。這種類型的架構有許多好處，包括減少設計時的耦合。 所涉及的應用程式都不了解其他應用程序，也不依賴其他應用程式。每個應用程式都會偵聽感興趣的主題，並根據它們執行的操作產生主題。它還可以透過添加可以使用相同事件而不影響現有流程的新應用程式來更輕鬆地擴展我們的系統。

由於 Kafka 中的事件是持久的，因此我們也可以稍後重播它們或使用它們來產生對組織其他部分有價值的資料產品。這可以取代部份的資料庫操作。

###### 運作範例

這裡是一個簡單的使用 Kafka 的 Microservices 範例，知道它使用的方式就可以思考一下在我們的狀況下那些運作可以參考應用。

開始時可透過 Web 應用程式訂購 Pizzas, 後端接到訂單後可以透過幾個微服務的運作按順序開始製作 Pizza,逐一添加醬料、起司、肉類及蔬菜，然後 Web 前台可查詢訂單狀態。

此範例由以下 5 個微服務依序完成披薩訂單的製作:

* Pizza-service 一個支援 Kafka 的 Flask Web 應用程式。可透過 Web 接受訂單及查詢訂單狀態。
* Sauce-service 是具有 Kafka Producer 與 Consumer 的基本應用程式。接到訂單後依序為 Pizza 添加醬料，然後往下一個流程送出訂單。
* Cheese-service 是具有 Kafka Producer 與 Consumer 的基本應用程式。接收前一個流程，添加起司後往下一個流程送出訂單。
* Meat-service 是具有 Kafka Producer 與 Consumer 的基本應用程式。接收前一個流程，添加肉類後往下一個流程送出訂單。
* veggie-service 是具有 Kafka Producer 與 Consumer 的基本應用程式。接收前一個流程，添加蔬菜後訂單完成往下一個流程送出，訂單完成。

在執行此示範之前，您需要建立 5 個 Kafka Topic 主題：

> pizza, pizza-with-sauce, pizza-with-cheese, pizza-with-meat, 與 pizza-with-veggies。

啟動微服務:

```
python3 ./app.py
python3 ./sauce_service.py
python3 ./cheese_service.py
python3 ./meat_service.py
python3 ./veggie_service.py
```

一旦所有五個微服務都啟動並運行，您就可以發出以下curl 命令來發送 2 個隨機披薩的訂單。

```
curl -X POST http://localhost:5000/order/2
```

這將觸發一系列事件，從而產生包含兩個披薩的披薩訂單，並且它將返回該披薩訂單的 UUID 編號。

```
{"order_id": "173296392152586628283665456967923585434"}
```

然後可以用這披薩的訂單編號來查詢訂購的訂單。

```
curl http://localhost:5000/order/{{pizza-order-UUID}}
```

例如:

```
curl http://localhost:5000/order/173296392152586628283665456967923585434
```

```
{
    "id": "173296392152586628283665456967923585434",
    "count": 2,
    "pizzas": [
        {
            "order_id": "173296392152586628283665456967923585434",
            "sauce": "淡",
            "cheese": "three cheese",
            "meats": "義大利辣香腸 & 香腸 & sausage",
            "veggies": "tomato & peppers & 鳳梨 & 蘑菇"
        },
        {
            "order_id": "173296392152586628283665456967923585434",
            "sauce": "light",
            "cheese": "特加乳酪",
            "meats": "pepperoni",
            "veggies": "胡椒 & pineapple & 蘑菇 & olives"
        }
    ]
}
```
