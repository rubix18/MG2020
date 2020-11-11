git clone https://github.com/rubix18/MG2020.git

cd ~/MG2020
source tflite1-env/bin/activate

sudo apt-get install libatlas-base-dev
pip3 install -r requirements.txt

echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

sudo apt-get update

sudo apt-get install libedgetpu1-std

pip3 install https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.5.0-cp37-cp37m-linux_armv7l.whl

sudo apt upgrade libedgetpu1-std

pip3 install https://dl.google.com/coral/python/tflite_runtime-2.1.0-cp37-cp37m-linux_armv7l.whl’.