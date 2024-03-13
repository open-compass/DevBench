package com.sohu.idcenter;

import org.junit.jupiter.api.Test;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashSet;
import java.util.Set;

/**
 * @author liuqi
 * @date 2023/12/11
 */
public class IdTest {
    @Test
    public void testIdWorker() {
        final long idepo = System.currentTimeMillis() - 3600 * 1000L;
        IdWorker iw = new IdWorker(1, 1, 0, idepo);
        IdWorker iw2 = new IdWorker(idepo);
        Set<Long> set1 = new HashSet<>();
        Set<Long> set2 = new HashSet<>();
        for (int i = 0; i < 1000; i++) {
            Long id1 = iw.getId();
            Long id2 = iw2.getId();
            assert !set1.contains(id1) && !set2.contains(id2);
            assert id1 > 0 && id2 > 0;
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


    private boolean checkSidWorkerId(Long id) throws ParseException {
        String dateStr = String.valueOf(id).substring(0, 17);
        SimpleDateFormat format = new SimpleDateFormat("yyyyMMddHHmmssSSS");
        Date d = format.parse(dateStr);
        Date now = new Date();
        return d.compareTo(now) <= 0;
    }

    @Test
    public void testSidWorker() throws ParseException {
        long st = System.currentTimeMillis();
        final int max = 100;
        Set<Long> ids = new HashSet<>();
        for (int i = 0; i < max; i++) {
            Long id = SidWorker.nextSid();
            assert id > 0;
            assert !ids.contains(id) : "i = " + i;
            assert checkSidWorkerId(id);
            ids.add(id);
        }
        long et = System.currentTimeMillis();
        System.out.println(1000 * max / (et - st) + "/s");
    }

}
