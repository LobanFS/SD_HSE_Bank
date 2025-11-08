from typing import Iterable, Mapping

def print_table(rows: Iterable[Mapping], columns: list[tuple[str, str]]):
    rows = list(rows)
    headers = [h for _, h in columns]
    data = []
    for r in rows:
        row_data = []
        for k, _ in columns:
            if hasattr(r, k):
                row_data.append(str(getattr(r, k)))
            elif isinstance(r, dict) and k in r:
                row_data.append(str(r[k]))
            else:
                row_data.append("")
        data.append(row_data)

    widths = [len(h) for h in headers]
    for row in data:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def line(ch="-"):
        print("+" + "+".join(ch * (w + 2) for w in widths) + "+")

    line()
    print("| " + " | ".join(h.ljust(w) for h, w in zip(headers, widths)) + " |")
    line("=")

    for row in data:
        print("| " + " | ".join(cell.ljust(w) for cell, w in zip(row, widths)) + " |")
    line()
