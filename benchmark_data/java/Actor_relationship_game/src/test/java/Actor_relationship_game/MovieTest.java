package Actor_relationship_game;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class MovieTest {
    @Test
    void testMovieIdAndTitle() {
        Movie movie = new Movie("301", "Example Movie");
        assertEquals("301", movie.getId());
        assertEquals("Example Movie", movie.getTitle());
    }

    @Test
    void testActorIds() {
        Movie movie = new Movie("302", "Another Movie");
        movie.getActorIds().add("101");
        movie.getActorIds().add("102");
        assertTrue(movie.getActorIds().contains("101"));
        assertTrue(movie.getActorIds().contains("102"));
    }
}
