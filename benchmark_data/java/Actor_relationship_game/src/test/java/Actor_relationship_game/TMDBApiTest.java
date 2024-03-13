package Actor_relationship_game;

import org.junit.jupiter.api.Test;

import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;

public class TMDBApiTest {
    private final TMDBApi tmdbApiReference = new TMDBApi();
    private final TMDBApi tmdbApiTest = new TMDBApi();

    @Test
    public void testGetMoviesByActorId() throws IOException {
        // Known actor ID (example: ID of a famous actor)
        String actorId = "123";

        // Get the reference response
        String referenceResponse = tmdbApiReference.getMoviesByActorId(actorId);
        // Get the test response
        String testResponse = tmdbApiTest.getMoviesByActorId(actorId);

        // Compare the two responses
        assertEquals(referenceResponse, testResponse);
    }

    @Test
    public void testSearchPopularActors() throws IOException {
        // Get the reference response
        String referenceResponse = tmdbApiReference.searchPopularActors();
        // Get the test response
        String testResponse = tmdbApiTest.searchPopularActors();

        // Compare the two responses
        assertEquals(referenceResponse, testResponse);
    }
}
