# Использование
У реализованного API две ручки:
1. **/api/rates**
Не принимает никаких параметров - просто возвращает список доступных валют
2. **/api/convert**
Принимает 3 параметра - _from_, _to_ и _amount_. Реализована проверка на корректность заданных параметров

## Установка и запуск через docker
Перейдите в папку с проектом и выполните команду ```
docker build -t converter .```

Далее, выполните команду ```
docker run converter```

Готово, API запущено, теперь можно отправлять запросы. Например, через postman или vs code (в файле req.rest) есть примеры запросов, необходимо расширение REST

Адрес для запросов **http://127.0.0.1:5000**
