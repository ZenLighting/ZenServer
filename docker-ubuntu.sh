sudo docker build ./ --tag zenserver:0.1.0 -f ./dockerfile
sudo docker run --network host -d zenserver:0.1.0