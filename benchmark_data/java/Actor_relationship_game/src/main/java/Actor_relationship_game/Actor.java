package Actor_relationship_game;

import java.io.Serializable;
import java.util.HashSet;
import java.util.Set;

public class Actor implements Serializable{
    private static final long serialVersionUID=1L;
    private String id;
    private String name;
    private Set<String> movieIds; // Store movie IDs

    public Actor(String id, String name) {
        this.id = id;
        this.name = name;
        this.movieIds = new HashSet<>();
    }

    // Getters and setters
    public Set<String> getMovieIds() {
        return movieIds;
    }
    public String getId() {
        return id;
    }
    public String getName() {
        return name;
    }
    public void setId(String id) {
        this.id = id;
    }
    public void setMovieIds(Set<String> movieIds) {
        this.movieIds = movieIds;
    }
    public void setName(String name) {
        this.name = name;
    }
}
