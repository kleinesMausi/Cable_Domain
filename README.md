# Cable Domain

An homage to the Cellular Automaton Wireworld.
This project is a custom implementation of Wireworld, built with a focus on usability and building complex circuits through a Blueprint System.


## Features

Blueprint System: Select parts of your circuit, save them with custom names, and reuse them like building blocks.

UI: A toggleable sidebar for tool selection and blueprint management.


## Logic Rules

The simulation follows the standard Wireworld rules:
1.  **Empty** -> Remains Empty.
2.  **Electro** -> Becomes Tail.
3.  **Tail** -> Becomes Cable.
4.  **Cable** -> Becomes Electro if exactly 1 or 2 neighbors are Electro.


## Requirements

This project uses **pygame-ce** (Community Edition).
```bash
pip install pygame-ce
```

## Execution

Navigate to the project directory and run:
```bash
python main.py
```

## Controls

| Key               | Action                                                |
| :---              | :---                                                  |
| `1` - `5`         | Switch Tools (Cable, Tail, Electro, Select, Paste)    |
| `Space`           | Pause / Resume Simulation                             |
| `S`               | Save selected area as Blueprint (while in Paste mode) |
| `E`               | Toggle "Save Electro" (Keep state when copying)       |
| `Ctrl` + `+/-`    | Zoom In / Out                                         |
| `WASD` / `Arrows` | Move Camera                                           |
| `Left Click`      | Place cell / Use tool                                 |
| `Right Click`     | Delete Cell                                           |