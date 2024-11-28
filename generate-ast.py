#!/usr/bin/env python

from pathlib import Path
import sys
from textwrap import indent, dedent


def main():
    if len(sys.argv) != 2:
        print("Usage: generate-ast.py <output directory>", file=sys.stderr)
        sys.exit(64)
    output_dir = sys.argv[1]
    define_ast(output_dir, "Expr", [
      "Binary   : Expr left, Token operator, Expr right",
      "Grouping : Expr expression",
      "Literal  : object value",
      "Unary    : Token operator, Expr right"
    ])

def define_ast(output_dir: str, base_name: str, types: list[str]):
    pass

    path = Path(output_dir) / f"{base_name.lower()}.py"
    with path.open("w") as writer:
        writer.write(dedent(f"""\
            from dataclasses import dataclass

            from token import Token

            class {base_name}():
                def accept(visitor: "Visitor"):
                    raise NotImplementedError()

        """))

        # The AST classes.
        for type in types:
            class_name = type.split(":")[0].strip()
            fields = type.split(":")[1].strip()
            define_type(writer, base_name, class_name, fields)

        define_visitor(writer, base_name, types)


def define_visitor(writer, base_name: str, types: list[str]):
    writer.write("class Visitor:\n")
    for type in types:
        type_name = type.split(":")[0].strip()
        writer.write(
            f"    def visit_{type_name.lower()}_{base_name.lower()}("
            f"self, {base_name.lower()}: {type_name}):\n"
            "        raise NotImplementedError()\n\n")


def define_type(writer, base_name: str, class_name: str, fields: list[str]):
    writer.write(dedent(f"""\
        @dataclass
        class {class_name}({base_name}):
    """))
    for field in fields.split(","):
        member_type, member_name = field.split()
        writer.write(f"    {member_name}: {member_type}\n")

    # Visitor pattern.
    writer.write(indent(prefix="    ", text=dedent(f"""
        def accept(self, visitor: "Visitor"):
            return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)

        """)))

if __name__ == "__main__":
    main()