package test;

import code.LeftistHeap;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class LeftistHeapTest {

    @Test
    void testLeftistHeap() {
        LeftistHeap heap = new LeftistHeap();
        Assertions.assertTrue(heap.isEmpty());
        heap.insert(6);
        Assertions.assertFalse(heap.isEmpty());
        heap.insert(2);
        heap.insert(3);
        heap.insert(1);
        heap.in_order();
        Assertions.assertEquals("[6, 2, 3, 1]", heap.in_order().toString());
        Assertions.assertEquals(1, heap.extract_min());
        Assertions.assertEquals("[6, 2, 3]", heap.in_order().toString());
        heap.insert(8);
        heap.insert(12);
        heap.insert(4);
        Assertions.assertEquals("[8, 3, 12, 2, 6, 4]", heap.in_order().toString());
        heap.clear();
        Assertions.assertTrue(heap.isEmpty());
    }
}
