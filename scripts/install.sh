branch=${1:-master}
path=${2:-/opt}

echo "Installing dependencies..."
sudo apt update
sudo apt install git -y
sudo apt install curl -y
sudo apt install python3 -y
sudo apt install python3-pip -y
sudo apt install tmux -y
sudo pip3 install flask
sudo pip3 install requests
sudo pip3 install argparse

echo "Installing CI-Dashboard..."
sudo rm -rf ${path}/ci-dashboard
sudo git clone -b ${branch} https://github.com/ahmedelsayed-93/ci-dashboard ${path}/ci-dashboard
sudo echo 'config.json' > ${path}/ci-dashboard/.gitignore
sudo chmod -R a+rwX ${path}/ci-dashboard
sudo cp ${path}/ci-dashboard/scripts/cidashboard.sh /usr/bin/cidashboard
sudo chmod +x /usr/bin/cidashboard
sudo echo ${path} > /etc/ci-dashboard.config 

echo "Done, for help type : 'cidashboard help in terminal'"


