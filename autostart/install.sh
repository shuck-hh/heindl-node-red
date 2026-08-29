# 1. Copy
sudo cp cpp.service /etc/systemd/system/
sudo cp py.service /etc/systemd/system/
sudo rm -f /etc/systemd/system/heindl-update.service

# 2. Reload
sudo systemctl daemon-reload

# 3. Enable
sudo systemctl enable cpp.service
sudo systemctl enable py.service
sudo systemctl disable heindl-update.service

# 4. Start
sudo systemctl start py.service
sudo systemctl start cpp.service