nohup redis-server >/dev/null 2>&1 &
./gradlew test
redis-cli SHUTDOWN