import requests
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MTMxNzA4NDQsIm5iZiI6MTcxMzE3MDg0NCwiZXhwIjoxNzQ0NzA2ODQ0LCJqdGkiOjY1NjI1MTB9.Fc2FYDKEpcIW8sc6V5ccY5su81BE61L6DGtpWUwdjTs'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}',
}
r2 = requests.get(url=f'https://www.sima-land.ru/api/v3/item/?category_id={207}', headers=headers)
print(r2.json())