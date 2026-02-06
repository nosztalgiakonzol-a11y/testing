# Redirect Tracker - Egyszerű verzió

Egyszerű program, ami megnyit egy URL-t a böngészőben, követi a redirect-et, és kiírja a végső URL-t a konzolra.

## Használat

```bash
python redirect_tracker.py
```

## Mit csinál?

1. Megnyitja a böngészőt (Chrome)
2. Betölti a megadott URL-t
3. Várja a redirect-et (3 másodperc)
4. Kiírja a végső URL-t a CMD-be

## Teszt URL-ek

A program két URL-t tesztel:
- `http://boabet.com/hu`
- `https://www.sportfogadas.org:2096/irodak/most`

## Kimenet példa

```
======================================================================
REDIRECT TRACKER - Egyszerű verzió
======================================================================
Chrome verzió: 144

======================================================================
Kezdő URL: http://boabet.com/hu
======================================================================
Böngésző megnyitása...

✓ VÉGSŐ URL: https://example.com/final-page

======================================================================
Kezdő URL: https://www.sportfogadas.org:2096/irodak/most
======================================================================
Böngésző megnyitása...

✓ VÉGSŐ URL: https://redirected-page.com

======================================================================
ÖSSZEFOGLALÓ
======================================================================

1. Oldal:
   Kezdő:  http://boabet.com/hu
   Végső:  https://example.com/final-page

2. Oldal:
   Kezdő:  https://www.sportfogadas.org:2096/irodak/most
   Végső:  https://redirected-page.com

======================================================================
```

## Követelmények

- Python 3.7+
- Chrome böngésző
- Dependencies: `pip install -r requirements.txt`
