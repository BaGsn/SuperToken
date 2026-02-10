# Super Token

Super Token is a simple plugin for **Glyphs App 3** that extends the standard **Token** system by allowing more powerful glyph-name operations.

In particular, Super Tokens make it possible to **replace, remove, or rename parts of glyph names** directly inside token expressions. This enables dynamic classes that automatically stay up to date when glyphs are added or removed.

---

## Syntax

The syntax of a Super Token is very similar to a regular Token, except that it takes an `S` after the `$` and before the brackets:

- Regular Token:

```text
$[ ... ]
```

- Super Token:

```text
$S[ ... ]
```

---

## Examples

Super Tokens can be used to define dynamic classes.

### Basic selection

Define a class `@def` containing all glyphs whose names end with `.001`:

```text
$S[name endswith '.001']
```

### Remove part of the name

Define a class `@sub` containing the same glyphs, but with `.001` removed from their names:

```text
$S[name endswith '.001' remove '.001']
```

### Rename part of the name

You can also rename a suffix into another one.  
For example, replacing `.001` with `.ss01`:

```text
$S[name endswith '.001' rename '.001' by '.ss01']
```

---

## Automatic Updates

The result is that if any glyph is added or removed, the list of glyphs in the classes will be updated automatically, just like with regular Glyphs Tokens.

---

## Usage in Glyphs App

Because Super Tokens are not supported by default in Glyphs App 3, they **cannot be used directly in the regular Feature panel** without triggering errors.

To work around this limitation:

- Write your Super Token source code in the **Notes panel**
- Super Token will automatically compile it into the Feature panel when you **Save**

---

## Stylistic Sets Limitation

Since the Notes panel is normally used to name Stylistic Sets, this means:

- Stylistic Sets cannot currently be used directly together with Super Tokens

---

## Current Limitations

For now, **Super Tokens are limited to `name` tokens only**.  
More token types may be supported in the future.

---

## References

- Glyphs App Tokens documentation:  
  https://glyphsapp.com/learn/tokens
