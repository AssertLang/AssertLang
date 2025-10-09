pub fn count() -> i32 {
    let x = 0;
    {
        let i = 0;
        while (i < 10) {
            x = (x + 1);
            i = (i + 1);
        }
    }
    return x;
}

pub fn sum_range(n: i32) -> i32 {
    let total = 0;
    {
        let i = 0;
        while (i < n) {
            total = (total + i);
            i = (i + 1);
        }
    }
    return total;
}
