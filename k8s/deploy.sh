kubectl apply -f ingres-config.yaml --namespace ingress-nginx
kubectl apply -f etcd.yaml --namespace ingress-nginx
kubectl apply -f book-info-deployment.yaml --namespace ingress-nginx
kubectl apply -f book-manager-deployment.yaml --namespace ingress-nginx
kubectl apply -f login-register-deployment.yaml --namespace ingress-nginx
