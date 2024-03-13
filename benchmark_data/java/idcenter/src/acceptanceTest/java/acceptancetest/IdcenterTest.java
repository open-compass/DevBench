package acceptancetest;

import com.sohu.idcenter.Base62;
import com.sohu.idcenter.IdWorker;
import com.sohu.idcenter.SidWorker;
import org.junit.jupiter.api.Test;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashSet;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;


public class IdcenterTest {

    private boolean checkSidWorkerId(Long id) throws ParseException {
        String dateStr = String.valueOf(id).substring(0, 17);
        SimpleDateFormat format = new SimpleDateFormat("yyyyMMddHHmmssSSS");
        Date d = format.parse(dateStr);
        Date now = new Date();
        return d.compareTo(now) <= 0;
    }

    @Test
    public void testIdWorker() {
        Set<Long> set1 = new HashSet<>();
        Set<Long> set2 = new HashSet<>();
        final long idepo = System.currentTimeMillis() - 3600 * 1000L;
        IdWorker iw = new IdWorker(1, 1, 0, idepo);
        IdWorker iw2 = new IdWorker(idepo);
        for (int i = 0; i < 10000; i++) {
            long id1 = iw.getId();
            long id2 = iw2.getId();
            assert id1 > 0 && id2 > 0;
            assertNotEquals(id1, id2);
            assert !set1.contains(id1);
            assert !set2.contains(id2);
            set1.add(id1);
            set2.add(id2);
        }
        System.out.println(iw);
        System.out.println(iw2);
        long nextId = iw.getId();
        System.out.println(nextId);
        long time = iw.getIdTimestamp(nextId);
        System.out.println(time + " -> " + new SimpleDateFormat("yyyyMMddHHmmss").format(new Date(time)));
    }


    @Test
    public void testSidWorker() throws ParseException {
        long st = System.currentTimeMillis();
        final int max = 100;
        Set<Long> ids = new HashSet<>();
        for (int i = 0; i < max; i++) {
            Long id = SidWorker.nextSid();
            assert !ids.contains(id) : "i = " + i;
            assert id > 0;
            assert checkSidWorkerId(id);
            ids.add(id);
        }
        long et = System.currentTimeMillis();
        System.out.println(1000 * max / (et - st) + "/s");
    }

    @Test
    public void testBase62() {
        assertEquals("1ly7vk", Base62.encode(1234567890L));
        assertEquals("aMoY42", Base62.encode(9876543210L));
        assertEquals("2H22RM", Base62.encode(2468135790L));
        assertEquals("1tTIeY", Base62.encode(1357924680L));
        assertEquals("9qRmlR", Base62.encode(8642097531L));
        assertEquals("7KHcLD", Base62.encode(7102938465L));
        assertEquals("6fEJjO", Base62.encode(5728149360L));
        assertEquals("2IZvXC", Base62.encode(2497085316L));
        assertEquals("56Jmnr", Base62.encode(4680132957L));
        assertEquals("a9uTqt", Base62.encode(9301678245L));
        assertEquals(1234567890L, Base62.decode("1ly7vk"));
        assertEquals(9876543210L, Base62.decode("aMoY42"));
        assertEquals(2468135790L, Base62.decode("2H22RM"));
        assertEquals(1357924680L, Base62.decode("1tTIeY"));
        assertEquals(8642097531L, Base62.decode("9qRmlR"));
        assertEquals(7102938465L, Base62.decode("7KHcLD"));
        assertEquals(5728149360L, Base62.decode("6fEJjO"));
        assertEquals(2497085316L, Base62.decode("2IZvXC"));
        assertEquals(4680132957L, Base62.decode("56Jmnr"));
        assertEquals(9301678245L, Base62.decode("a9uTqt"));
    }
}
