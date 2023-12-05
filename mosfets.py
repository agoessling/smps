import argparse
import os
from typing import Sequence

import pandas as pd
import rapidfuzz as rf


def find_column(cols: Sequence[str] | pd.Index, terms: list[str], cutoff: int=0) -> str | None:
  matches = []
  for t in terms:
    match = rf.process.extractOne(t, cols)
    if match is None:
      continue
    if match[1] < cutoff:
      continue
    matches.append(match)

  matches.sort(key=lambda x: x[1], reverse=True)
  print(matches)

  if not matches:
    return None

  return matches[0][0]


def find_part_number(df: pd.DataFrame) -> pd.Series:
  match = find_column(df.columns, ['part', 'part number', 'product', 'series'], 70)
  if match is None:
    raise RuntimeError(f'Part number not found in {df.columns}')

  return match


def parse_mosfet_dir(vendor: str, dir: str) -> pd.DataFrame:
  df = pd.DataFrame()

  for file in os.listdir(dir):
    if os.path.splitext(file)[1] != '.csv':
      continue
    table = pd.read_csv(os.path.join(dir, file))
    print(find_part_number(table))

  return df


def parse_vendor_dirs(dir: str) -> pd.DataFrame:
  df = pd.DataFrame()
  for entry in os.scandir(dir):
    if not entry.is_dir():
      continue
    vendor = entry.name
    dir = entry.path
    df = pd.concat((df, parse_mosfet_dir(vendor, dir)))

  return df


def main():
  parser = argparse.ArgumentParser(description='Extract and/or view MOSFET database.')
  parser.add_argument('--directory', '-d', help='Directory of vendor folders.')

  args = parser.parse_args()

  if args.directory and not os.path.isdir(args.directory):
    parser.error(f'{args.directory} is not a valid directory.')

  if args.directory:
    parse_vendor_dirs(args.directory)


if __name__ == '__main__':
  main()
