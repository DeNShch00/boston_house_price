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
1. Склонировать содержимое [course_project](https://github.com/DeNShch00/geekbrains/tree/ml_business/ml_business/course_project) себе на машину. 
2. Запустить на выполнение ноутбук **model/model.ipynb**. В результате будет получен файл с моделью **model/boston-model.dill** и файл со средними значениями характеристик **model/boston-features-avg.csv**.
3. Перейти в папку **app/** и запустить создание Docker-образа:

    ```
    docker build -t boston .
    ```
4. Запустить Docker-контейнер на основе созданного образа. Пробросить локальный порт 8080 на порт контейнера 8080. Подключить VOLUME с локально созданной на шаге 2 моделью к каталогу /usr/src/app/mode контейнера:

    ```
    docker run --rm -d -p 8080:8080 -v <path_to_model>:/usr/src/app/model boston
    ```
5. С помощью утилиты curl выполнить POST -запрос к сервису, передав JSON-строку с заданными характеристиками недвижимости:

    ```
    curl -i -H "Content-type: application/json" -X POST -d "{"RM":1, "LSTAT":33.3}" http://localhost:8080/predict
    ```
