import sys

def reverse_od(content):
    res = bytearray()
    for line in content.strip().split('\n'):
        parts = line.split()
        if not parts: continue
        # Ignore the first part (offset)
        for p in parts[1:]:
            try:
                val = int(p, 8)
                # od -o uses 2-byte shorts
                # We need to figure out the byte order. 
                # Usually it's native. Let's try little-endian.
                res.append(val & 0xFF)
                res.append((val >> 8) & 0xFF)
            except ValueError:
                continue
    return res

if __name__ == "__main__":
    with open("whatisthis.baboi", "r") as f:
        content = f.read()
    decoded = reverse_od(content)
    try:
        print(decoded.decode('utf-8'))
    except:
        print(decoded)
