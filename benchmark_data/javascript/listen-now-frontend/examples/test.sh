# build for production with minification
rm -rf node_modules
rm chromedriver_linux64.zip
export PATH=$PATH:$(pwd)/node_modules/phantomjs-prebuilt/lib/phantom/bin/
wget https://chromedriver.storage.googleapis.com/2.46/chromedriver_linux64.zip
npm install
npm run build
export OPENSSL_CONF=/dev/null
npm run unit
