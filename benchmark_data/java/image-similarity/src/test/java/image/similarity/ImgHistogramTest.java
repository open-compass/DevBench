package image.similarity;

import java.io.File;
import java.io.IOException;
import java.net.URL;

import image.similarity.ImageHistogram;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class ImgHistogramTest {

    ImageHistogram histogram = new ImageHistogram();

    @Test
    public void testImageHistogram() {
        try {
            double score = histogram.match(new File("imgs/1.jpg"), new File("imgs/1.jpg"));
            System.out.println("img1-->img1::::score : " + score);
            Assertions.assertTrue(score >= 0.8);

            score = histogram.match(new File("imgs/1.jpg"), new File("imgs/2.jpg"));
            System.out.println("img1-->img2::::score : " + score);
            Assertions.assertTrue(score >= 0.8);

            score = histogram.match(new File("imgs/1.jpg"), new File("imgs/3.jpg"));
            System.out.println("img1-->img3::::score : " + score);
            Assertions.assertTrue(score >= 0.8);

            score = histogram.match(new File("imgs/1.jpg"), new File("imgs/4.jpg"));
            System.out.println("img1-->img4::::score : " + score);
            Assertions.assertTrue(score < 0.8);

            score = histogram.match(new File("imgs/5.jpg"), new File("imgs/6.jpg"));
            System.out.println("img5-->img6::::score : " + score);
            Assertions.assertTrue(score < 0.8); // incorrect

            score = histogram.match(new File("imgs/1.jpg"), new File("imgs/6.jpg"));
            System.out.println("img1-->img6::::score : " + score);
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

}
