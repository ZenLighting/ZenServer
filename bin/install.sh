# check that python 3 is installed

if ! command -v python3.8 &> /dev/null
then
    echo "COMMAND could not be found"
    exit
fi

#check python3 version
var=$(python3.8 -V)
if [$var != "Python 3.8.5"]; then
    echo "Python 3.8.5 is not installed"
    echo $var
    exit
else
    echo "Python 3.8.5 is installed"
fi

# create directory in /opt/
sudo mkdir /opt/ZenLighting
echo $USER
sudo chown $USER /opt/ZenLighting

#change working directory to /opt/ZenLighting
cd /opt/ZenLighting
rm -Rf ZenServer
echo $(ls)
git clone https://github.com/ZenLighting/ZenServer.git
echo $(ls ./ZenServer)
cd /opt/ZenLighting/ZenServer
echo $(pwd)
python3.8 -m pip install virtualenv
python3.8 -m venv venv
echo $(ls)
source venv/bin/activate
pip install -r requirements.txt

#place service into correct dir
sudo cp ./bin/zenserver.service /lib/systemd/system/zenserver.service