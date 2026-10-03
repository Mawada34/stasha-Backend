import requests

TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc4OTU1MDEyMiwianRpIjoiZjhkNTY5NTUtOWRjZC00Nzk3LWI1MGYtNzAyNzQyNGM2OGQyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzg5NTUwMTIyLCJjc3JmIjoiM2RmOGZhMjItMTVkYS00NzI2LWExN2MtNDMzZjVkNmY2NmFjIiwiZXhwIjoxNzg5NTUxMDIyfQ.dQD7AVIeKTNXmpZjtgKlbnEDPbxbEQrOZROXl6G66bU"
FILE_PATH=r"C:\Users\T490s\Downloads\Screenshot 2026-05-20 034348.png"

url="http://127.0.0.1:5000/api/upload/"
headers={"Authorization":f"Bearer {TOKEN}"}

with open(FILE_PATH, "rb") as f:
    files = {"file": f}
    response = requests.post(url, headers=headers, files=files)

print("Status code:", response.status_code)
print("Response:", response.json())