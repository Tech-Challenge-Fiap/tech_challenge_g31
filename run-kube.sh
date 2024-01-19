#!/bin/bash


helm package fiaptechchallenge
helm install fiaptechchallenge-0.1.0.tgz --generate-name
rm fiaptechchallenge-0.1.0.tgz

trap "helm uninstall $(helm list --filter 'fiaptechchallenge' --no-headers --short)" INT

running=false
while [ "$running" = false ]; do
    echo "waiting pod to be ready..."
    r=$(kubectl wait --for=condition=ready pod -l app=fiaptechchallenge)
    if [[ "$r" == *"condition met"* ]]; then
        running=true
    fi
done
echo "pod is running"
kubectl wait --for=condition=ready pod -l app=fiaptechchallenge
kubectl port-forward service/svcfiaptechchallenge 5000:80
echo 'visit http://localhost:5000 to access the service'    