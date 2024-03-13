package Actor_relationship_game;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import static org.junit.jupiter.api.Assertions.*;

class ActorGraphTest {
    private ActorGraph graph;

    @BeforeEach
    void setUp() {
        graph = new ActorGraph();
        // Adding sample actors
        graph.addActor(new Actor("101", "John Doe"));
        graph.addActor(new Actor("102", "Jane Smith"));
        // Adding a sample movie
        graph.addMovie(new Movie("301", "Example Movie"));
        // Connecting actors to the movie
        graph.addActorToMovie("101", "301");
        graph.addActorToMovie("102", "301");
    }

    @Test
    void testAddActor() {
        assertNotNull(graph.getActors().get("101"));
        assertEquals("John Doe", graph.getActors().get("101").getName());
    }

    @Test
    void testAddMovie() {
        assertNotNull(graph.getMovies().get("301"));
        assertEquals("Example Movie", graph.getMovies().get("301").getTitle());
    }

    @Test
    void testAddActorToMovie() {
        assertTrue(graph.getActors().get("101").getMovieIds().contains("301"));
        assertTrue(graph.getMovies().get("301").getActorIds().contains("101"));
    }

    @Test
    void testFindConnectionWithPath() {
        List<Map.Entry<String, String>> connectionPath = graph.findConnectionWithPath("101", "102");
        assertFalse(connectionPath.isEmpty(), "The connection path should not be empty.");
        assertEquals("John Doe", connectionPath.get(0).getKey(), "First actor in the path should be John Doe.");
        assertEquals("Jane Smith", connectionPath.get(1).getKey(), "Second actor in the path should be Jane Smith.");
        assertEquals("Example Movie", connectionPath.get(1).getValue(), "Jane Smith should be connected through 'Example Movie'.");
    }

}
