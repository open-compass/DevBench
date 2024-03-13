package Actor_relationship_game;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.*;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class ActorGraphUtilTest {

    private final String testFilePath = "./src/test/java/Actor_relationship_game/test_actors_list.txt";
    private final String testGraphPath = "./src/test/java/Actor_relationship_game/test_actorGraph.ser";

    @BeforeEach
    void setUp() throws IOException {
        // Create a test ActorGraph object and serialize it
        ActorGraph actorGraph = new ActorGraph();
        actorGraph.addActor(new Actor("101", "John Doe"));
        actorGraph.addActor(new Actor("102", "Jane Smith"));

        try (FileOutputStream fileOut = new FileOutputStream(testGraphPath);
             ObjectOutputStream out = new ObjectOutputStream(fileOut)) {
            out.writeObject(actorGraph);
        }
    }

    @AfterEach
    void tearDown() {
        // Clean up the test files
        new File(testFilePath).delete();
        new File(testGraphPath).delete();
    }

    @Test
    void testLoadGraph() {
        ActorGraph loadedGraph = ActorGraphUtil.loadGraph(testGraphPath);
        assertNotNull(loadedGraph, "Loaded graph should not be null");
        assertEquals(2, loadedGraph.getActors().size(), "Loaded graph should have 2 actors");
    }

    @Test
    void testWriteActorsToFile() throws IOException {
        List<String> actorNames = Arrays.asList("John Doe", "Jane Smith");
        ActorGraphUtil.writeActorsToFile(actorNames, testFilePath);

        try (BufferedReader reader = new BufferedReader(new FileReader(testFilePath))) {
            assertEquals("John Doe", reader.readLine(), "First line should be John Doe");
            assertEquals("Jane Smith", reader.readLine(), "Second line should be Jane Smith");
        }
    }
}
