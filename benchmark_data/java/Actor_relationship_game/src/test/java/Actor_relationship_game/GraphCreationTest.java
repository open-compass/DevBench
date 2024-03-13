package Actor_relationship_game;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.FileInputStream;
import java.io.ObjectInputStream;

import static org.junit.jupiter.api.Assertions.*;

public class GraphCreationTest {
    private GraphCreation graphCreation;
    String testGraphPath;

    @BeforeEach
    public void setUp() {
        graphCreation = new GraphCreation();
        testGraphPath = "./src/test/java/Actor_relationship_game/test_actorGraph.ser";
    }

    @AfterEach
    void tearDown() {
        // Clean up the test files
        new File(testGraphPath).delete();
    }

    @Test
    public void testCreateGraph() {
        assertDoesNotThrow(() -> graphCreation.createGraph(testGraphPath),
                "Graph creation should not throw any exceptions.");
    }

    @Test
    public void testGraphFileCreation() {
        assertDoesNotThrow(() -> graphCreation.createGraph(testGraphPath),
                "Graph creation should create a file without exceptions.");

        File file = new File(testGraphPath);
        assertTrue(file.exists(), "File actorGraph.ser should exist after graph creation.");
    }

    @Test
    public void testGraphFileContent() {
        assertDoesNotThrow(() -> graphCreation.createGraph(testGraphPath),
                "Graph creation should create a file without exceptions.");

        File file = new File(testGraphPath);
        assertTrue(file.exists(), "File actorGraph.ser should exist after graph creation.");

        try (FileInputStream fileIn = new FileInputStream(testGraphPath);
             ObjectInputStream in = new ObjectInputStream(fileIn)) {
            ActorGraph actorGraph = (ActorGraph) in.readObject();
            assertNotNull(actorGraph, "ActorGraph object should not be null.");
            assertFalse(actorGraph.getActors().isEmpty(), "ActorGraph should contain actors.");
            assertFalse(actorGraph.getMovies().isEmpty(), "ActorGraph should contain movies.");
        } catch (Exception e) {
            fail("Exception should not be thrown while reading the actorGraph.ser file.");
        }
    }
}
