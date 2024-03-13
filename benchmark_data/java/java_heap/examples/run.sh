#!/bin/bash
./gradlew clean
./gradlew build -x test
./gradlew run
