from parsimonious.grammar import Grammar

# This grammar is used to parse the PNG data from generic thumbnail declarations
grammar = Grammar(r"""
  Document   = Thumbnail+
  Thumbnail  = Header Payload+ Footer

  #                                  width   x   height      size
  Header     = "; thumbnail begin " Integer "x" Integer " " Integer newline
  Payload    = "; " Base64 newline
  Base64     = ~"[A-Za-z0-9+/]*={0,2}"
  Footer     = "; thumbnail end" newline

  Integer    = ~r"\d+"
  newline    = ~r"\r?\n"
""")
