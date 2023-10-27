from typing import List, Tuple

def parse_command(raw_command: str) -> Tuple[str, List[str]]:
  tokens = raw_command.strip().split()
  
  operation = tokens[0].upper()
  arguments = tokens[1:]
  
  return operation, arguments