
curl -v -H "Host: sklearn-iris.kserve-test.example.com" -H "Content-Type: application/json" http://localhost:8080/v1/models/sklearn-iris:predict -d @./iris-input.json

mainly make sure you pass content type here 
