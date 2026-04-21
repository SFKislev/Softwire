# Sources

- Autodesk MAXScript Help, `Quick Navigation - Main Index` (entrypoint for section crawls):
  https://help.autodesk.com/cloudhelp/2017/ENU/MAXScript-Help/files/GUID-D986BA05-E8EF-4CD4-8CFC-8325D5D91104.htm
- Autodesk MAXScript Help, `3ds MAX Commands` (official command table):
  https://help.autodesk.com/cloudhelp/2017/ENU/MAXScript-Help/files/GUID-A96857E7-73FE-4F42-BE71-E8185356F4C9.htm
- Autodesk MAXScript Help, `Class and Object Inspector Functions` (inspection/discovery functions):
  https://help.autodesk.com/cloudhelp/2024/ENU/MAXScript-Help/files/3ds-Max-Objects-and-Interfaces/Identifying-and-Accessing/GUID-879ECFAD-7928-44B3-BCD7-276D53C89B52.html

## Extraction

- Date: 2026-04-21
- Method: crawled official MAXScript-Help section pages from the Quick Navigation index, then mechanically parsed code/pre blocks and page text patterns for symbols.
- Normalization: one symbol per line, deduplicated, whitespace-normalized.

## Counts

- CLASS: 857
- INTERFACE: 178
- PROPERTY: 54
- METHOD: 779
- MAX_COMMAND: 222
- MXS_FUNCTION: 11
- RUNTIME_DISCOVERY: 5
