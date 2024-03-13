/**
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 * <p>
 * http://www.apache.org/licenses/LICENSE-2.0
 * <p>
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.sohu.idcenter;


import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * @author adyliu (imxylz@gmail.com)
 * @since 2012-8-7
 */
public class Base62Test {

    /**
     * Test method for {@link com.sohu.idcenter.Base62#encode(long)}.
     */
    @Test
    public void testEncode() {
        assertEquals("1IwymnQs", Base62.encode(6050648952832L));
    }

    /**
     * Test method for {@link com.sohu.idcenter.Base62#decode(java.lang.String)}.
     */
    @Test
    public void testDecode() {
        assertEquals(6050648952832L, Base62.decode("1IwymnQs"));
    }

}