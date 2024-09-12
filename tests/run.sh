cd $(dirname $0)
cd ../

python3 -m unittest -v tests.TestConfig
python3 -m unittest -v tests.TestUtils
python3 -m unittest -v tests.TestRetriableDecorator