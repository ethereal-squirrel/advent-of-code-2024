def main():
    d = open('input').read().strip()
    b, f, i = [], 0, 0
    while i < len(d):
        b += [str(f)] * int(d[i]) + ['.'] * (int(d[i+1]) if i+1 < len(d) else 0)
        f, i = f + 1, i + 2
    p = {int(c): [] for c in b if c != '.'}
    for i, c in enumerate(b):
        if c != '.': p[int(c)].append(i)
    for f, pos in sorted(p.items(), key=lambda x: -x[0]):
        l = len(pos)
        for s in range(len(b) - l + 1):
            if all(c == '.' for c in b[s:s + l]):
                for i in range(l): b[s + i] = str(f)
                for i in pos: b[i] = '.'
                break
            if s > pos[0]: break
    print(sum(i * int(c) for i, c in enumerate(b) if c != '.'))

if __name__ == "__main__":
    main()