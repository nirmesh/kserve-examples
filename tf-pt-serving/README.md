kubectl get isvc flower-sample 
MODEL_NAME=flower-sample
INPUT_PATH=@./input.json
SERVICE_HOSTNAME=$(kubectl get inferenceservice ${MODEL_NAME} -o jsonpath='{.status.url}' | cut -d "/" -f 3)
echo $SERVICE_HOSTNAME
 kubectl port-forward  --address localhost,10.118.169.62  svc/istio-ingressgateway -n istio-system 8080:80 &

curl -v -H "Host: ${SERVICE_HOSTNAME}" -H "Content-Type: application/json" http://localhost:8080/v1/models/$MODEL_NAME:predict -d $INPUT_PATH

### for pytorch

kubectl apply -f torchserve.yaml
MODEL_NAME=mnist
SERVICE_HOSTNAME=$(kubectl get inferenceservice torchserve -o jsonpath='{.status.url}' | cut -d "/" -f 3)
curl -v -H "Host: ${SERVICE_HOSTNAME}" -H "Content-Type: application/json" http://localhost:8080/v1/models/${MODEL_NAME}:predict -d @./mnist.json


