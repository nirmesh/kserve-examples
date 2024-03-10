
curl -v -H "Host: kserve-custom-model.default.example.com" http://localhost:8080/v1/models/kfserving-custom-model:predict  -d @./qa_bert_input.json

mainly make sure v1/models/<model-name> should be from your python file
