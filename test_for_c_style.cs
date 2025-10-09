using System;

namespace Main
{
    public static class Functions
    {
        public static int Count()
        {
            var x = 0;
            for (var i = 0;; (i < 10); i = (i + 1);)
            {
                x = (x + 1);
            }
            return x;
        }

        public static int SumRange(int n)
        {
            var total = 0;
            for (var i = 0;; (i < n); i = (i + 1);)
            {
                total = (total + i);
            }
            return total;
        }

    }

}
