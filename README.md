# Тестовое задание от Aviata & Chocotravel

1. Создать базу данных и юзера с привелегией над базой
2. Создать .env как на примере([.env_example](https://github.com/moldabek/SkyPickerWeb/blob/main/.env_example))
3. Следущем шагом создать образ и запустить
   1. `docker build -t <name_of_image> .`
   2. `docker run -d --network host --name <name_of_runner> <name_of_image>`
   3. `docker logs -f <name_of_runner>`
# Endpoint-ы для взаимодейтсвие с данными в базе
1. `<HOST>:<PORT>/get_tickets/` - отображение билетов и их данных в json формате
>Метод запроса: GET

Запрос: Не передается

Ответ:
```json
{
   "25/10/2021": {
           "ALA-TSE": {
               "price": 265122,
               "booking_token": "some_booking_token"
           }
           ...
      }
   ...
}
```

3. `<HOST>:<PORT>/check_tickets/` - проверка валидности билета
>Метод запроса: GET

Запрос:
```json
{
   "ticket_date": "25/10/2021",
   "fly_from": "ALA",
   "fly_to": "TSE"
}
```
Ответ при успешном запросе:
```json
{
   "valid": true,
   "booking_token": "some_booking_token"
}
```
Ответ при неуспешном запросе:
```json
{
   "data": "booking_token doesn't exist"
}
```
