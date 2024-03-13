# run the actor relationship game


./gradlew runGraphCreation -PfileName="./src/main/java/Actor_relationship_game/actorGraph.ser"
./gradlew runActorGraphUtil -PgraphPath="./src/main/java/Actor_relationship_game/actorGraph.ser" -PfilePath="./src/main/java/Actor_relationship_game/actors_list.txt"
./gradlew runGamePlayInterface -PgraphPath="./src/main/java/Actor_relationship_game/actorGraph.ser" -PactorPath="./src/main/java/Actor_relationship_game/actors_list.txt" -PfilePath="./src/main/java/Actor_relationship_game/actor_connection_results.txt"