# Data Mining in Dblp.org

homework of datamining

# File Structure
- `dataset` *all the databases should be stored in this folder, formatted as sqlite3*
- `scripts`
  - `dbgenerate.py` *used to generate the database automatically*
- `lib` this folder contains all main codes
  - `conn.py` an encapsulated module, used to apply query on textual databases
  - `fptree.py` describes how to construct a fp-tree
  - `fpgrowth.py` fp-growth algorithm
- `test` several trivial testing scripts
- `hw1.py` the main file of the first homework

# Timeline
- *Mar 17th, 2016* start!
- *Mar 18th, 2016* bug fixed when crawling journal papers
- *Mar 19th, 2016* fp-tree's constructing algorithm finished
- *Apr 5th, 2016* the fp-growth algorithm has been finished