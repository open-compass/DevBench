package Actor_relationship_game;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ActorTest {
    @Test
    void testActorIdAndName() {
        Actor actor = new Actor("101", "John Doe");
        assertEquals("101", actor.getId());
        assertEquals("John Doe", actor.getName());
    }

    @Test
    void testMovieIds() {
        Actor actor = new Actor("102", "Jane Smith");
        actor.getMovieIds().add("201");
        actor.getMovieIds().add("202");
        assertTrue(actor.getMovieIds().contains("201"));
        assertTrue(actor.getMovieIds().contains("202"));
    }
}
