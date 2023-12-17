sudo docker run --name chislash \
    --network="host" \
    --privileged \
    --rm -itd \
    -v $HOME/.config/chislash:/etc/clash \
    -v /dev:/dev \
    -v /lib/modules:/lib/modules \
    chisbread/chislash:latest
