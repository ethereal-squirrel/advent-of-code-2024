def main():
    d = open('input').read().strip()
    b, f, i = [], 0, 0
    while i < len(d):
        b += [str(f)] * int(d[i]) + ['.'] * (int(d[i+1]) if i+1 < len(d) else 0)
        f, i = f + 1, i + 2
    for r in range(len(b) - 1, -1, -1):
        if b[r] != '.':
            for w in range(r):
                if b[w] == '.':
                    b[w], b[r] = b[r], b[w]
                    break
    print(sum(p * int(c) for p, c in enumerate(b) if c != '.'))

if __name__ == "__main__":
    main()