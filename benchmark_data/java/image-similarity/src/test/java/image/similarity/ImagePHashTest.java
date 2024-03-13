package image.similarity;

import image.similarity.ImagePHash;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.net.URL;

/**
 * Unit test for simple App.
 */
public class ImagePHashTest {
    ImagePHash p = new ImagePHash();

    @Test
    public void testImgPHash() {
        try {
            int dis = p.distance(new File("imgs/1.jpg"), new File("imgs/1.jpg"));
            System.out.println("img1-->img1::::distance:" + dis);
            Assertions.assertTrue(dis < 10);

            dis = p.distance(new File("imgs/1.jpg"), new File("imgs/2.jpg"));
            System.out.println("img1-->img2::::distance:" + dis);
            Assertions.assertTrue(dis > 10); // incorrect

            dis = p.distance(new File("imgs/1.jpg"), new File("imgs/3.jpg"));
            System.out.println("img1-->img3::::distance:" + dis);
            Assertions.assertTrue(dis > 10); // incorrect

            dis = p.distance(new File("imgs/2.jpg"), new File("imgs/3.jpg"));
            System.out.println("img2-->img3::::distance:" + dis);
            Assertions.assertTrue(dis < 10);

            dis = p.distance(new File("imgs/2.jpg"), new File("imgs/4.jpg"));
            System.out.println("img2-->img4::::distance:" + dis);
            Assertions.assertTrue(dis > 10);

            dis = p.distance(new File("imgs/1.jpg"), new File("imgs/4.jpg"));
            System.out.println("img2-->img3::::distance:" + dis);
            Assertions.assertTrue(dis > 10);

            String srcUrl = "http://oarfc773f.bkt.clouddn.com/100000094nzslsdnswbb_1_1_r.jpg";
            dis = p.distance(new URL("https://img3.doubanio.com/lpic/s27140981.jpg"), new URL(srcUrl));
            System.out.println("url::::distance:" + dis);
            Assertions.assertTrue(dis < 10);

            dis = p.distance(new URL("https://img3.doubanio.com/lpic/s8966044.jpg"), new URL(srcUrl));
            System.out.println("url::::distance:" + dis);
            Assertions.assertTrue(dis < 10);

        } catch (Exception e) {
            e.printStackTrace();
        }

    }

}
