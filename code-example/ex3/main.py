import tabulate
import symtable

code ="""
a = 1
b = 2

defer:
    a += 2
"""

_st = symtable.symtable(code, "example.py", "exec")

def show(table):
    print("Symtable {0}".format(table.get_name()))
    
    print(
        tabulate.tabulate(
            [
                (
                    symbol.get_name(),
                    symbol.is_global(),
                    symbol.is_local(),
                    symbol.get_namespaces(),
                )
                for symbol in table.get_symbols()
            ],
            headers=["name", "global", "local", "namespaces"],
            tablefmt="grid",
        )
    )
    if table.has_children():
        [show(child) for child in table.get_children()]


show(_st)