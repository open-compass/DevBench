package Actor_relationship_game;

import java.io.Serializable;
import java.util.HashSet;
import java.util.Set;

public class Movie implements Serializable {
    private static final long serialVersionUID=1L;

    private String id;
    private String title;
    private Set<String> actorIds; // Store actor IDs

    public Movie(String id, String title) {
        this.id = id;
        this.title = title;
        this.actorIds = new HashSet<>();
    }

    // Getters and setters
    public String getId() {
        return id;
    }
    public Set<String> getActorIds() {
        return actorIds;
    }
    public String getTitle() {
        return title;
    }
    public void setId(String id) {
        this.id = id;
    }
    public void setActorIds(Set<String> actorIds) {
        this.actorIds = actorIds;
    }
    public void setTitle(String title) {
        this.title = title;
    }

}

