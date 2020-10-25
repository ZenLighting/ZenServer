sudo docker build ./ --tag zenserver:0.1.0 -f ./arm.dockerfile
sudo docker run --network host zenserver:0.1.0