kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.9.5/deploy/static/provider/cloud/deploy.yaml
kubectl apply -f ingres-config.yaml --namespace ingress-nginx
kubectl apply -f etcd.yaml --namespace ingress-nginx
kubectl apply -f book-info-deployment.yaml --namespace ingress-nginx
kubectl apply -f book-manager-deployment.yaml --namespace ingress-nginx
kubectl apply -f login-register-deployment.yaml --namespace ingress-nginx
kubectl apply -f openapi-deployment.yaml --namespace ingress-nginx
