# Square Wave Generator
The square wave generator is a simple function block to provide a square wave output for given high and low times.
The notation used is similar to timers. It is created with function blocks.

It has been uploaded in XML format meaning that it can be imported by right clicking on _Function & Function Blocks_ and selecting _Import IEC 61131-10..._. It can therefore be edited once imported.

## Inputs
IN - BOOL - Enable the wave generator.
PTH - TIME- Preset time in High
PTL - TIME - Preset time in Low

## Outputs
Q - Square wave output
ETH - TIME - Elapsed time in high
ETL - TIME - Elapsed time in low
