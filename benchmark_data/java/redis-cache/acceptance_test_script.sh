nohup redis-server >/dev/null 2>&1 &
./gradlew acceptanceTest
redis-cli SHUTDOWN