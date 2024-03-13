nohup redis-server >/dev/null 2>&1 &
./gradlew test
./gradlew acceptanceTest
./gradlew shadowJar
java -jar redis-cache-1.0-all.jar input.txt output.txt
redis-cli SHUTDOWN
