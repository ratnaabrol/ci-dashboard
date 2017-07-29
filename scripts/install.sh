branch=${1:-itsyouonline-auth}
path=${2:-/opt}

echo "Installing dependencies..."
apt update
apt install git -y
apt install curl -y
apt install python3 -y
apt install python3-pip -y
apt install tmux -y
pip3 install flask
pip3 install requests
pip3 install argparse

echo "Installing CI-Dashboard..."
rm -rf ${path}/ci-dashboard
git clone -b ${branch} https://github.com/ahmedelsayed-93/ci-dashboard ${path}/ci-dashboard
echo 'config.json' > ${path}/ci-dashboard/.gitignore
chmod -R a+rwX ${path}/ci-dashboard
cp ${path}/ci-dashboard/scripts/cidashboard.sh /usr/bin/cidashboard
chmod +x /usr/bin/cidashboard
echo ${path} > /etc/ci-dashboard.config 

echo "Done, for help type : 'cidashboard help'"


