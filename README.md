# Сервис прогнозирования цены на недвижимость в Бостоне

## Введение

Сервис позволяет спрогнозировать цену на недвижимость по заданным характеристикам недвижимости.
Для прогнозирования сервис использует заранее обученную модель.
Взаимодействие с сервисом происходит посредством отправки ему JSON-документа с характеристиками через REST API, в ответ сервис отправляет JSON-документ с прогнозом цены. Если какая-то характеристика не задана, то сервис заполняет её средним значением, посчитанным из датасета, на котором обучалась модель.

## Модель

> [model.ipynb](https://github.com/DeNShch00/geekbrains/blob/ml_business/ml_business/course_project/model/model.ipynb)

Модель представляет из себя регрессию, определяющую цену на недвижимость, в качестве алгоритма  взят RandomForestRegressor.
Модель обучена на встроенном в **sklearn.datasets** датасете, который можно получить, вызвав метод **load_boston**. 
В качестве характеристик недвижимости выступают следующие:

>  1. CRIM:     per capita crime rate by town
>  2. ZN:       proportion of residential land zoned for lots over 25,000
>     sq.ft.
>  3. INDUS:    proportion of non-retail business acres per town
>  4. CHAS:     Charles River dummy variable (= 1 if tract bounds river; 0
>     otherwise)
>  5. NOX:      nitric oxides concentration (parts per 10 million)
>  6. RM:       average number of rooms per dwelling
>  7. AGE:      proportion of owner-occupied units built prior to 1940
>  8. DIS:      weighted distances to five Boston employment centres
>  9. RAD:      index of accessibility to radial highways
>  10. TAX:      full-value property-tax rate per $10,000
>  11. PTRATIO:  pupil-teacher ratio by town
>  12. B:        1000(Bk - 0.63)^2 where Bk is the proportion of blacks by
>      town
>  13. LSTAT:    % lower status of the population
>  14. MEDV :    Median value of owner-occupied homes in $1000's

Все характеристики имеют вещественное значение.
В JSON-документе, подаваемом на вход сервису, имена характеристик соответствуют именам, представленным выше.
Наиболее влияющими на цену характеристиками являются RM и LSAT (см. работу по определению вклада характеристик по методу SHAP - [lesson7_homework](https://github.com/DeNShch00/geekbrains/blob/ml_business/ml_business/lesson%207/HW7.ipynb)):
 - чем больше процент населения с "низким" статусом проживает в данном
   районе (признак LSTAT), тем цена домов ниже
 - чем больше количество комнат в доме (признак RM), тем его цена выше

Именно их и рекомендуется задавать сервису в качестве исходных данных.

## Запуск сервиса
1. Склонировать содержимое репозитория себе на машину:

    ```
    git clone https://github.com/DeNShch00/boston_house_price.git
    ```
2. Запустить на выполнение ноутбук **model/model.ipynb**. В результате будет получен файл с моделью **model/boston-model.dill** и файл со средними значениями характеристик **model/boston-features-avg.csv**.
3. Перейти в папку **app/** и запустить создание Docker-образа (!!!В зависимости от пользователя ОС может потребоваться указывать sudo перед командами docker):

    ```
    docker build -t boston .
    ```
4. Запустить Docker-контейнер на основе созданного образа. Пробросить локальный порт **8080** на порт контейнера **8080**. Подключить VOLUME с локально созданной на шаге 2 моделью к каталогу **/usr/src/app/model** контейнера:

    ```
    docker run --rm -d -p 8080:8080 -v <path_to_model>:/usr/src/app/model boston
    ```
5. В браузере открыть страницу по адресу http://127.0.0.1:8080 чтобы убедиться, что сервер, запущенный в контейнере, отвечает. Он должен вернуть строку "Hello!".
6. С помощью утилиты **curl** выполнить POST-запрос к сервису, передав JSON-строку с заданными характеристиками недвижимости:

    ```
    curl -i -H "Content-type: application/json" -X POST -d "{\"RM\":1, \"LSTAT\":33.3}" http://localhost:8080/predict
    ```
     Пример ответа сервера:
     ```
     HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 446
    Server: Werkzeug/1.0.1 Python/3.9.4
    Date: Sat, 24 Apr 2021 15:16:42 GMT
    
    {
      "features": {
        "AGE": 68.57490118577078, 
        "B": 356.67403162055257, 
        "CHAS": 0.0691699604743083, 
        "CRIM": 3.6135235573122535, 
        "DIS": 3.795042687747034, 
        "INDUS": 11.136778656126504, 
        "LSTAT": 33.3, 
        "NOX": 0.5546950592885372, 
        "PTRATIO": 18.455533596837967, 
        "RAD": 9.549407114624506, 
        "RM": 55.0, 
        "TAX": 408.2371541501976, 
        "ZN": 11.363636363636363
      }, 
      "predict": 28.102200000000106
    }
    ```
