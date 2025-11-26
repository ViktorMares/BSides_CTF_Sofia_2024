# This lab was created for Security BSides Sofia 2024 by Viktor Mares   


# Installation & Usage (Docker)
```
git clone https://github.com/ViktorMares/BSides_CTF_Sofia_2024.git
```
```
cd BSides_CTF_Sofia_2024
```
```
docker compose up --build
```
```
access the app on http://0.0.0.0:8000
```
   
## Installation & Usage (Manual)
```
git clone https://github.com/ViktorMares/BSides_CTF_Sofia_2024.git
```
```
cd BSides_CTF_Sofia_2024
```
```
pip3 install -r requirements.txt
```
```
cd app
```
```
uvicorn main:app --reload
```

   
   
### Lab Objective:
Access the resource at <b>/admin</b> - to do this, you will need to exploit a misconfiguration of the current JWT implementation  

   
### API:
To explore and interact with the API, access the Swagger documentation at "/docs".
The documentation provides detailed information about available endpoints, request formats, and example responses.

