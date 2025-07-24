from block import Block

def fix_ruler(blocks: list[Block]):
    if len(blocks) <= 1:
        return blocks

    lengths = [(r - l + 1) for l, r in blocks]
    gaps = [(l - r - 1)
            for (_, r), (l, _) in zip(blocks, blocks[1:])]

    L = min(lengths)
    G = sum(gaps) / len(gaps)

    gaps.append(G)
    for (l, r), length in zip(blocks, lengths):
        k = max(1,
                round((length + G) / (L + G)))

        sing_len = (length - (k - 1) * G) / k

        yield from (
            (round(start := l + i * (L + G)),
             round(start + sing_len - 1))
            for i in range(k)
        )
