package Actor_relationship_game;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class GameplayInterfaceTest {

    private GameplayInterface gameplay;
    private ActorGraph testGraph;
    private String testOutputFilePath;

    @BeforeEach
    public void setup() {
        gameplay = new GameplayInterface();
        testGraph = createTestActorGraph();
        gameplay.setActorGraph(testGraph);
        testOutputFilePath = "./src/test/java/Actor_relationship_game/test_actor_connection_results.txt";
    }

    @AfterEach
    void tearDown() {
        // Clean up the test files
        new File(testOutputFilePath).delete();
    }

    private ActorGraph createTestActorGraph() {
        // Create a hardcoded ActorGraph based on your predefined actors and movies
        ActorGraph actorGraph = new ActorGraph();

        // Add actors
        Actor actorA = new Actor("A", "Actor A");
        Actor actorB = new Actor("B", "Actor B");
        Actor actorC = new Actor("C", "Actor C");
        Actor actorD = new Actor("D", "Actor D");
        Actor actorE = new Actor("E", "Actor E");

        // Add movies
        Movie movieAB = new Movie("AB", "Movie AB");
        Movie movieBC = new Movie("BC", "Movie BC");
        Movie movieCD = new Movie("CD", "Movie CD");
        Movie movieAC = new Movie("AC", "Movie AC");
        Movie movieAD = new Movie("AD", "Movie AD");
        Movie movieAE = new Movie("AE", "Movie AE");
        Movie movieBE = new Movie("BE", "Movie BE");
        Movie movieDE = new Movie("DE", "Movie DE");

        // Add actors to graph
        actorGraph.addActor(actorA);
        actorGraph.addActor(actorB);
        actorGraph.addActor(actorC);
        actorGraph.addActor(actorD);
        actorGraph.addActor(actorE);

        // Add movies to graph
        actorGraph.addMovie(movieAB);
        actorGraph.addMovie(movieBC);
        actorGraph.addMovie(movieCD);
        actorGraph.addMovie(movieAC);
        actorGraph.addMovie(movieAD);
        actorGraph.addMovie(movieAE);
        actorGraph.addMovie(movieBE);
        actorGraph.addMovie(movieDE);

        // Connect actors to movies
        actorGraph.addActorToMovie("A", "AB");
        actorGraph.addActorToMovie("B", "AB");
        actorGraph.addActorToMovie("B", "BC");
        actorGraph.addActorToMovie("C", "BC");
        actorGraph.addActorToMovie("C", "CD");
        actorGraph.addActorToMovie("D", "CD");
        actorGraph.addActorToMovie("A", "AC");
        actorGraph.addActorToMovie("C", "AC");
        actorGraph.addActorToMovie("A", "AD");
        actorGraph.addActorToMovie("D", "AD");
        actorGraph.addActorToMovie("A", "AE");
        actorGraph.addActorToMovie("E", "AE");
        actorGraph.addActorToMovie("B", "BE");
        actorGraph.addActorToMovie("E", "BE");
        actorGraph.addActorToMovie("D", "DE");
        actorGraph.addActorToMovie("E", "DE");

        return actorGraph;
    }

    @Test
    public void testFindConnections() throws IOException {
        List<String[]> actorPairs = generateAllActorPairs();
        gameplay.findConnections(actorPairs, testOutputFilePath);

        // Read the output file
        List<String> outputLines = Files.readAllLines(Paths.get(testOutputFilePath));

        // Verify the output against the hardcoded expected values
        verifyOutput(outputLines);
    }


    private void verifyOutput(List<String> outputLines) {
        // Hardcoded expected connection numbers for each pair
        Map<String, Integer> expectedConnectionNumbers = new HashMap<>();
        expectedConnectionNumbers.put("Actor A-Actor B", 1);
        expectedConnectionNumbers.put("Actor A-Actor C", 1);
        expectedConnectionNumbers.put("Actor A-Actor D", 1);
        expectedConnectionNumbers.put("Actor A-Actor E", 1);
        expectedConnectionNumbers.put("Actor B-Actor C", 1);
        expectedConnectionNumbers.put("Actor B-Actor D", 2);
        expectedConnectionNumbers.put("Actor B-Actor E", 1);
        expectedConnectionNumbers.put("Actor C-Actor D", 1);
        expectedConnectionNumbers.put("Actor C-Actor E", 2);
        expectedConnectionNumbers.put("Actor D-Actor E", 1);

        for (Map.Entry<String, Integer> entry : expectedConnectionNumbers.entrySet()) {
            String actors = entry.getKey().replace("-", " and ");
            Integer expectedNumber = entry.getValue();
            String expectedLine = "Connection Number between " + actors + ":" + expectedNumber;

            assertTrue(containsLine(outputLines, expectedLine), "Expected connection number line not found: " + expectedLine);
        }
    }

    private boolean containsLine(List<String> outputLines, String expectedLine) {
        return outputLines.stream().anyMatch(line -> line.trim().equals(expectedLine));
    }




    private List<String[]> generateAllActorPairs() {
        List<String> actorNames = Arrays.asList("Actor A", "Actor B", "Actor C", "Actor D", "Actor E");
        List<String[]> pairs = new ArrayList<>();

        for (int i = 0; i < actorNames.size(); i++) {
            for (int j = i + 1; j < actorNames.size(); j++) {
                pairs.add(new String[]{actorNames.get(i), actorNames.get(j)});
            }
        }

        return pairs;
    }
}
