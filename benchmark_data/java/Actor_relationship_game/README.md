# Actor Relationship Game

## Project Overview
The Actor Relationship Game is a Java-based application that allows users to explore connections between actors through their movie collaborations. Utilizing data from The Movie Database (TMDB) API, it constructs a graph of actors and identifies the shortest path of relationships between any two actors.

## Features
- Construct a graph of actors and movies using data from TMDB API.
- Explore relationships between actors.
- Find the shortest path between any two actors in the graph.

## Getting Started
### Prerequisites
- Java Runtime Environment (JRE)
- Gradle (for building the project)
- TMDB API Key (Get one from TMDB API: https://developer.themoviedb.org/docs/getting-started)
### Usage
To run the project, execute the following steps in order:
- 1. Graph Creation:

```bash
./gradlew runGraphCreation -PfileName="your/actorGraph/path/actorGraph.ser"
```
This step fetches data from TMDB API and constructs the actor graph.


- 2. ActorGraph Utility:
```bash
./gradlew runActorGraphUtil -PgraphPath="your/actorGraph/path/actorGraph.ser" -PfilePath="your/actors_list/path/actors_list.txt"
```
This step serializes the graph and prepares it for the gameplay interface.

- 3. Gameplay Interface:
```bash
./gradlew runActorGraphUtil -PgraphPath="your/actorGraph/path/actorGraph.ser" -PactorPath="your/actors_list/path/actors_list.txt" -PfilePath="your/results/path/actor_connection_results_test.txt"
```
In this final step, interact with the application to explore actor relationships.

## Acknowledgments
The Movie Database (TMDB) for providing the API used in this project.