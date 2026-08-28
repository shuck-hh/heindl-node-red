sudo cp cpp.service /etc/systemd/system/
sudo cp py.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable cpp.service
sudo systemctl enable py.service
sudo systemctl start py.service
sudo systemctl start cpp.service