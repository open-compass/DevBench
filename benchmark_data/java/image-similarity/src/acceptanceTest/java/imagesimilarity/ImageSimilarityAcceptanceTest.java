import image.similarity.ImageHistogram;
import image.similarity.ImagePHash;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.IOException;
import java.net.URL;

public class ImageSimilarityAcceptanceTest {
    @Test
    public void testHistogram() {
        ImageHistogram histogram = new ImageHistogram();
        try {
            double score = histogram.match(new File("imgs/1.jpg"), new File("imgs/1.jpg"));
            Assertions.assertTrue(score >= 0.8);

            score = histogram.match(new File("imgs/1.jpg"), new File("imgs/2.jpg"));
            Assertions.assertTrue(score >= 0.8);

            score = histogram.match(new File("imgs/1.jpg"), new File("imgs/3.jpg"));
            Assertions.assertTrue(score >= 0.8);

            score = histogram.match(new File("imgs/1.jpg"), new File("imgs/4.jpg"));
            Assertions.assertTrue(score < 0.8);

            score = histogram.match(new File("imgs/5.jpg"), new File("imgs/6.jpg"));
            Assertions.assertTrue(score < 0.8); // incorrect

            score = histogram.match(new File("imgs/1.jpg"), new File("imgs/6.jpg"));
            Assertions.assertTrue(score < 0.8);

            String srcUrl = "http://oarfc773f.bkt.clouddn.com/100000094nzslsdnswbb_1_1_r.jpg";
            score = histogram.match(new URL(srcUrl), new URL("https://img3.doubanio.com/lpic/s27140981.jpg"));
            System.out.println("url::::score:" + score);
            Assertions.assertTrue(score < 0.8);    // incorrect

            score = histogram.match(new URL(srcUrl), new URL("https://img3.doubanio.com/lpic/s8966044.jpg"));
            System.out.println("url::::score:" + score);
            Assertions.assertTrue(score < 0.8);    // incorrect

        } catch (IOException e) {
            e.printStackTrace();
            Assertions.assertFalse(false);
        }
    }

    @Test
    public void testPHash() {
        ImagePHash p = new ImagePHash();
        try {
            int dis = p.distance(new File("imgs/1.jpg"), new File("imgs/1.jpg"));
            Assertions.assertTrue(dis < 10);

            dis = p.distance(new File("imgs/1.jpg"), new File("imgs/2.jpg"));
            Assertions.assertTrue(dis > 10); // incorrect

            dis = p.distance(new File("imgs/1.jpg"), new File("imgs/3.jpg"));
            Assertions.assertTrue(dis > 10); // incorrect

            dis = p.distance(new File("imgs/2.jpg"), new File("imgs/3.jpg"));
            Assertions.assertTrue(dis < 10);

            dis = p.distance(new File("imgs/2.jpg"), new File("imgs/4.jpg"));
            Assertions.assertTrue(dis > 10);

            dis = p.distance(new File("imgs/1.jpg"), new File("imgs/4.jpg"));
            Assertions.assertTrue(dis > 10);

            String srcUrl = "http://oarfc773f.bkt.clouddn.com/100000094nzslsdnswbb_1_1_r.jpg";
            dis = p.distance(new URL("https://img3.doubanio.com/lpic/s27140981.jpg"), new URL(srcUrl));
            Assertions.assertTrue(dis < 10);

            dis = p.distance(new URL("https://img3.doubanio.com/lpic/s8966044.jpg"), new URL(srcUrl));
            Assertions.assertTrue(dis < 10);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
