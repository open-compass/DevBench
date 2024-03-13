package rediscache;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.mybatis.caches.redis.RedisCache;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;


public class RedisCacheAcceptanceTest {

    private static final String DEFAULT_ID = "REDIS";
    private static RedisCache cache;

    @BeforeAll
    static void newCache() {
        cache = new RedisCache(DEFAULT_ID);
    }

    @Test
    public void testPutAndGet() {
        Map<Integer, String> localCache = new HashMap<>();
        for (int i = 0; i < 100; i++) {
            Integer id = new Random().nextInt();
            String value = String.valueOf(new Random().nextDouble());
            cache.putObject(id, value);
            localCache.put(id, value);
        }
        for (Map.Entry<Integer, String> entry : localCache.entrySet()) {
            Integer id = entry.getKey();
            String value = entry.getValue();
            Object cacheValue = cache.getObject(id);
            cache.removeObject(id);
            assert cacheValue != null;
            assert (cacheValue).equals(value);
        }
    }
}