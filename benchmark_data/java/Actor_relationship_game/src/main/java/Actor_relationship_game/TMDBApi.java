package Actor_relationship_game;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import java.io.IOException;

public class TMDBApi {
    private final OkHttpClient client;
    private final String apiKey = System.getenv("TMDB_API_KEY"); // get API Key from environmental variable

    public TMDBApi() {
        this.client = new OkHttpClient();
    }

    public String getMoviesByActorId(String actorId) throws IOException {
        String url = "https://api.themoviedb.org/3/person/" + actorId + "/movie_credits?api_key=" + apiKey;
        Request request = new Request.Builder().url(url).build();

        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Unexpected code " + response);
            }
            return response.body().string();
        }
    }


    public String searchPopularActors() throws IOException {
        String url = "https://api.themoviedb.org/3/person/popular?api_key=" + apiKey;
        Request request = new Request.Builder().url(url).build();

        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Unexpected code " + response);
            }
            return response.body().string();
        }
    }


}
